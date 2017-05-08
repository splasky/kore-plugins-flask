import pytest


class TestApplication(object):

    @pytest.fixture
    def flask_view(self):
        def view():
            return "Hello World!"
        return view

    @pytest.mark.parametrize('methods', [
        ['GET', ], ['GET', 'POST'], ['GET', 'PUT'], ['GET', 'POST', 'PUT']
    ])
    def test_view(self, application, flask_view, methods):
        url = '/hello'
        application.add_url_rule(url, view_func=flask_view, methods=methods)
        client = application.test_client()

        rv = client.open(url, method='OPTIONS')
        data = client.get(url).data

        assert rv.status_code == 200
        assert sorted(rv.allow) == sorted(methods + ['HEAD', 'OPTIONS'])
        assert data == b"Hello World!"

    def test_application(self, application, flask_config):
        assert application.instance_path == flask_config['instance_path']
        assert application.root_path == flask_config['root_path']

        assert application.config['DEBUG'] == flask_config['DEBUG']
        assert application.config['SECRET_KEY'] == flask_config['SECRET_KEY']
