"""Index view unit test
"""
import pytest


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    """Setup hook
    """
    pass


def test_view_index_view_date_timezone(dummy_request, mocker):
    """Test index
    """
    import datetime

    class DummyDatetime(datetime.datetime):
        """Pesudo datetime class dummy_now is binded to this class
        """
        pass

    def dummy_now(_cls, tzinfo):
        """Returns datetime instance with timezone given as argument

        tzinfo is pytz.utc (python 2) or datetime.timezone.utc (>= python 3)
        """
        return datetime.datetime(2017, 7, 7, 9, 9, 9, tzinfo=tzinfo)

    mocker.patch.object(DummyDatetime, 'now')
    DummyDatetime.now = dummy_now.__get__(DummyDatetime)  # bind
    datetime.datetime = DummyDatetime

    from bregenz.views.action import index
    res = index(dummy_request)
    assert str == type(res['view_date'])
    # it must be in UTC
    assert '2017-07-07T09:09:09+00:00' == res['view_date']


def test_view_index(dummy_request):
    """Test index
    """
    from bregenz.views.action import index

    res = index(dummy_request)
    assert dict == type(res)
