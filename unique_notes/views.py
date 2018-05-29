from aiohttp import web
import aiohttp_jinja2

from . import db


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.note.select().order_by(db.note.c.unique_words.desc()))
        records = await cursor.fetchall()
        notes = [dict(n) for n in records]
        return {'notes': notes}


@aiohttp_jinja2.template('note_detail.html')
async def note_detail(request):
    async with request.app['db'].acquire() as conn:
        note_id = request.match_info['note_id']
        try:
            note = await db.get_note(conn, note_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {
            'note': note,
        }


@aiohttp_jinja2.template('note_create.html')
async def note_create_page(request):
    return {'error': None, 'form': None}


@aiohttp_jinja2.template('note_create.html')
async def note_create(request):
    async with request.app['db'].acquire() as conn:
        form = await request.post()
        if not form['title']:
            error = "Title can't be empty"
        elif not form['description']:
            error = "Description can't be empty"
        else:
            title = form['title']
            description = form['description']
            note_id = await db.note_create(conn, title, description)
            print(note_id)
            router = request.app.router
            location = router['note_detail'].url_for(note_id=str(note_id))
            return web.HTTPFound(location=location)
        return {'error': error, 'form': form}
