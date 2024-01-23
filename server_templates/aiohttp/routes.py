from .views import response__simplest_text


def setup_routes(app):
    app.router.add_get('/', response__simplest_text)
