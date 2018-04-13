# Default view properties


def test_default_response_portfolio_view(dummy_request):
    from ..views.default import my_portfolio_view

    response = my_portfolio_view(dummy_request)
    assert isinstance(response, dict)
    assert response['entries'] == []


def test_default_detail_view(dummy_request, db_session, test_stock):
    from ..views.default import my_detail_view

    db_session.add(test_stock)

    dummy_request.matchdict = {'symbol': 'AM'}
    response = my_detail_view(dummy_request)
    assert response['stock'].symbol == 'AM'
    assert type(response['stock'].companyName) == str


def test_detail_not_found(dummy_request):
    from ..views.default import my_detail_view
    from pyramid.httpexceptions import HTTPNotFound

    response = my_detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_default_response_stock_view(dummy_request):
    from ..views.default import my_stock_view

    response = my_stock_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


def test_valid_post_to_stock_view(dummy_request):
    from ..views.default import my_stock_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'symbol': "AM",
        'companyName': "ayymang",
        'exchange': "NYC",
        'industry': "dusty",
        'website': "google.com",
        'description': "test",
        'CEO': "me",
        'issueType': "huh",
        'sector': "three"
    }

    response = my_stock_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_valid_post_to_stock_view_adds_record_to_db(dummy_request, db_session):
    from ..views.default import my_stock_view
    from ..models import Stock

    dummy_request.method = 'POST'
    dummy_request.POST = {
        'symbol': "AM",
        'companyName': "ayymang",
        'exchange': "NYC",
        'industry': "dusty",
        'website': "google.com",
        'description': "test",
        'CEO': "me",
        'issueType': "huh",
        'sector': "three"
    }

    # assert right here that there's nothing in the DB

    my_stock_view(dummy_request)
    query = db_session.query(Stock)
    one = query.first()
    assert one.symbol == 'AM'
    assert one.companyName == 'ayymang'
    assert type(one.sector) == str


# def test_invalid_post_to_stock_view(dummy_request):
#     import pytest
#     from ..views.default import my_stock_view
#     from pyramid.httpexceptions import HTTPBadRequest

#     dummy_request.method = 'POST'
#     dummy_request.POST = {}

#     with pytest.raises(HTTPBadRequest):
#         response = my_stock_view(dummy_request)
#         assert isinstance(response, HTTPBadRequest)
