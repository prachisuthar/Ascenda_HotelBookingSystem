import pytest


paths = (
    '/',
    '/index2'
)


@pytest.mark.django_db()
@pytest.mark.parametrize('path', paths)
def test_xss_patterns(selenium, live_server, settings, xss_pattern, path):
    setattr(settings, 'XSS_PATTERN', xss_pattern.string)
    selenium.get('%s%s' % (live_server.url, path))
    assert not xss_pattern.succeeded(selenium), xss_pattern.message


@pytest.fixture(scope='session')
def session_capabilities(session_capabilities):
    session_capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

    return session_capabilities


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.headless = True
    return chrome_options