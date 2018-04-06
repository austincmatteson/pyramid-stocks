def test_default_behavior_of_home_view(dummy_request):
    from ..views.default import my_home_view

    request = dummy_request
    response = my_home_view(request)
    assert isinstance(response, dict)
    assert response == {}


def test_default_behavior_of_auth_view(dummy_request):
    from ..views.default import my_auth_view

    response = my_auth_view(dummy_request)
    assert isinstance(response, dict)
    assert response == {}


def test_default_behavior_of_portfolio_view(dummy_request):
    from ..views.default import my_portfolio_view

    response = my_portfolio_view(dummy_request)
    assert type(response) == dict
    assert response['entries'][0]['symbol'] == 'GE'


# def test_default_behavior_of_detail_view(dummy_request):
#     from ..views.default import my_detail_view

#     response = my_detail_view(dummy_request)
#     assert isinstance(response, dict)
#     assert response == {}


# def test_default_behavior_of_stock_view(dummy_request):
#     from ..views.default import my_stock_view

#     response = my_stock_view(dummy_request)
#     assert isinstance(response, dict)
#     assert response == {}
