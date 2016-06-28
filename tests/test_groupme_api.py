"""
Implements basic tests against the GroupMe API implementation.
"""
import pytest
from pytest_localserver.http import WSGIServer
import groupme_mock_server

def pytest_funcarg__groupme_api_server(request):
    """
    Creates a PyTest functional argument out of Flask WSGI server mockup.
    """
    server = WSGIServer(application=groupme_mock_server.app)
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
    assert groupme_api.get('') == {'text': 'Hello, world!'}


