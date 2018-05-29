import pathlib

from .views import index, note_detail, note_create, note_create_page

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/notes/create/', note_create_page, name='note_create_page')
    app.router.add_get('/notes/{note_id}/', note_detail, name='note_detail')
    app.router.add_post('/notes/create/', note_create, name='note_create')
    setup_static_routes(app)


def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=PROJECT_ROOT / 'static',
                          name='static')
