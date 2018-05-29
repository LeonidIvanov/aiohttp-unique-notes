import logging

from aiohttp import web
import jinja2
import aiohttp_jinja2

from .settings import config
from .middlewares import setup_middlewares
from .routes import setup_routes
from .db import init_pg, close_pg


def init():
    app = web.Application()
    app['config'] = config

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('unique_notes', 'templates'))

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    setup_routes(app)
    setup_middlewares(app)

    return app


def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    app = init()
    web.run_app(app)


if __name__ == '__main__':
    main()
