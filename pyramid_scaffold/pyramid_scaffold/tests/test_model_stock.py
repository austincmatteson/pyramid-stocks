def test_constructed_stock_added_to_database(db_session):
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol="AM",
        companyName="ayymang",
        exchange="NYC",
        industry="dusty",
        website="google.com",
        description="test",
        CEO="me",
        issueType="huh",
        sector="tc"
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_constructed_stock_with_no_sector_added_to_database(db_session):
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol="AM",
        companyName="ayymang",
        exchange="NYC",
        industry="dusty",
        website="google.com",
        description="test",
        CEO="me",
        issueType="huh"
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_stock_with_no_symbol_throws_error(db_session):
    from ..models import Stock
    import pytest
    from sqlalchemy.exc import IntegrityError

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        companyName="ayymang",
        exchange="NYC",
        industry="dusty",
        website="google.com",
        description="test",
        CEO="me",
        issueType="huh",
        sector="tc"
    )
    with pytest.raises(IntegrityError):
        db_session.add(stock)

        assert db_session.query(Stock).one_or_none() is None
