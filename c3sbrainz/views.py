from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

import musicbrainzngs

from .models import (
    DBSession,
    MyModel,
    )

@view_config(route_name='status', renderer='templates/status.pt')
def status_view(request):
    bar = 25
    output = ''
    hostname = '192.168.54.101:5000'
    musicbrainzngs.set_hostname(hostname)
    musicbrainzngs.auth("user", "password")
    musicbrainzngs.set_useragent(
        'c3sbrainz',
        '0.1a',
        'dev@c3s.cc'
        )
    artistid = "952a4205-023d-4235-897c-6fdb6f58dfaa"
    #import pdb
    #pdb.set_trace()
    print(dir(musicbrainzngs))
    #output = dir(musicbrainzngs)
    output = musicbrainzngs.get_artist_by_id(artistid)
    print  musicbrainzngs.get_artist_by_id(artistid)
    return {
        'foo': 'foo',
        'bar': bar,
        'hostname': hostname,
        'output': output
        }

@view_config(route_name='search', renderer='templates/search.pt')
def search_view(request):
    bar = 25
    #import pdb
    #pdb.set_trace()
    return {
        'foo': 'foo',
        'bar': bar}

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'c3sbrainz'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_c3sbrainz_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

