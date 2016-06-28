import pytest
from pytest_localserver.http import WSGIServer
import groupme_mock

def pytest_funcarg__groupme_api_server(request):
    """

    """
    server = WSGIServer(application=groupme_mock.app)
    server.start()
    request.addfinalizer(server.stop)
    return server

@pytest.fixture
def groupme_api(groupme_api_server):
    import groupcurses.groupme_api
    api = groupcurses.groupme_api.GroupMeAPI('1234')
    api.base_url = groupme_api_server.url
    return api

def test_get(groupme_api, groupme_api_server):
    groupme_api.get('')


