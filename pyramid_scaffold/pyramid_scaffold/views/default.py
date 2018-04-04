from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel


@view_config(route_name='home', renderer='../templates/index.jinja2')
def my_home_view(request):
    return {}


@view_config(route_name='auth', renderer='../templates/register.jinja2')
def my_auth_view(request):
    return {}


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2')
def my_stock_view(request):
    return {}


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def my_portfolio_view(request):
    return {}


@view_config(route_name='detail', renderer='../templates/stock-detail.jinja2')
def my_detail_view(request):
    return {}


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
