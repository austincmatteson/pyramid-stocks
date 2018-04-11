from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
import requests
from sqlalchemy.exc import DBAPIError, IntegrityError
from ..models import Stock, Account
from pyramid.httpexceptions import (HTTPFound, HTTPNotFound, HTTPBadRequest,
                                    HTTPUnauthorized, HTTPConflict)


API_URL = 'https://api.iextrading.com/1.0'


@view_config(
    route_name='home',
    renderer='../templates/index.jinja2',
    request_method='GET',
    permission=NO_PERMISSION_REQUIRED)
def my_home_view(request):
    return {}


@view_config(
    route_name='auth',
    renderer='../templates/auth.jinja2',
    permission=NO_PERMISSION_REQUIRED)
def my_auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']

        except KeyError:
            return {}

        is_authenticated = Account.check_credentials(
            request, username, password)
        if is_authenticated[0]:
            headers = remember(request, userid=username)
            return HTTPFound(location=request.route_url('portfolio'),
                             headers=headers)
        else:
            return HTTPUnauthorized()

    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
        except KeyError:
            return HTTPBadRequest()

        try:
            instance = Account(
                username=username,
                email=email,
                password=password,
            )

            headers = remember(request, userid=instance.username)
            try:
                request.dbsession.add(instance)
                request.dbsession.flush()
            except IntegrityError:
                return HTTPConflict()
            return HTTPFound(location=request.route_url('portfolio'),
                             headers=headers)

        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)

    return HTTPNotFound()


@view_config(
    route_name='portfolio',
    renderer='../templates/portfolio.jinja2',
    request_method='GET')
def my_portfolio_view(request):
    try:
        query = request.dbsession.query(Stock)
        all_entries = query.all()
    except DBAPIError:
        return DBAPIError(db_err_msg, content_type='text/plain', status=500)

    return {'entries': all_entries}


@view_config(
    route_name='stock',
    renderer='../templates/stock-add.jinja2')
def my_stock_view(request):
    if request.method == 'POST':
        fields = ['companyName', 'symbol', 'exchange', 'website', 'CEO',
                  'industry', 'sector', 'issueType', 'description']
        if not all([field in request.POST for field in fields]):
            return HTTPBadRequest()

        try:
            stock = {
                'companyName': request.POST['companyName'],
                'symbol': request.POST['symbol'],
                'exchange': request.POST['exchange'],
                'website': request.POST['website'],
                'CEO': request.POST['CEO'],
                'industry': request.POST['industry'],
                'sector': request.POST['sector'],
                'issueType': request.POST['issueType'],
                'description': request.POST['description'],
            }
            stock = Stock(**stock)
        except KeyError:
            pass

        try:
            request.dbsession.add(stock)
            request.dbsession.flush()
        except IntegrityError:
            return HTTPConflict()

        return HTTPFound(location=request.route_url('portfolio'))

    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}

        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        return {'company': data}

    else:
        raise HTTPNotFound()


@view_config(
    route_name='detail',
    renderer='../templates/stock-detail.jinja2',
    request_method='GET')
def my_detail_view(request):
    try:
        stock = request.matchdict['symbol']
    except (KeyError, IndexError):
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        entry_detail = query.filter(Stock.symbol == stock).first()
    except DBAPIError:
        return DBAPIError(db_err_msg, content_type='text/plain', status=500)
    return {"stock": entry_detail}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_scaffold_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
