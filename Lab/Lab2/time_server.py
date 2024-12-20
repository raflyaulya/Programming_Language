from wsgiref.simple_server import make_server
from datetime import datetime
from dateutil import tz
import json
import requests

# define the WSGI Application
def application(environ, start_response):
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']

    if path == '/' and method == 'GET':
        # Handle GET / request
        return handle_get_root(environ, start_response)
    
    elif path.startswith('/') and method =='GET':
        # handle GET / <tz name> request
        return handle_get_timezone(environ, start_response)
    
    elif path == '/api/v1/time' and method== 'POST':
        # Handle POST /api/v1/time request
        return handle_post_time(environ, start_response)
    
    elif path == '/api/v1/date' and method == 'POST':
        # handle POST /api/v1/date request
        return handle_post_date(environ, start_response)
    
    elif path == '/api/v1/datediff' and method == 'POST':
        # handle POST /api/v1/datediff request
        return handle_post_datediff(environ, start_response)
    
    else:
        # handle invalid request
        status = '404 Not Found'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Not Found\n']
    
# Helper Functions for each request type
def handle_get_root(environ, start_response):
    """
    Handles GET / request: Returns current time in server's timezone.
    """
    now = datetime.now()
    server_tz = tz.gettz()  # Get server's timezone
    now_server_time = now.astimezone(server_tz)
    html = f"<h1>Current time in {server_tz}: {now_server_time.strftime('%Y-%m-%d %H:%M:%S %z')}</h1>"
    status = '200 OK'
    headers = [('Content-Type', 'text/html')]
    start_response(status, headers)
    return [html.encode('utf-8')]

def handle_get_timezone(environ, start_response):
    """
    Handles GET /<tz name> request: Returns current time in specified timezone.
    """
    try:
        tz_name = environ['PATH_INFO'][1:]  # Extract timezone name from URL
        tz_obj = tz.gettz(tz_name)
        now = datetime.now()
        now_tz_time = now.astimezone(tz_obj)
        html = f"<h1>Current time in {tz_name}: {now_tz_time.strftime('%Y-%m-%d %H:%M:%S %z')}</h1>"
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        return [html.encode('utf-8')]
    except:
        status = '404 Not Found'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Invalid timezone\n']


# handle_post_time
def handle_post_time(environ, start_response):
    """
    Handles POST /api/v1/time request: Returns current time in specified timezone (or server's timezone).
    """
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(request_body)
        tz_name = data.get('tz') 

        if tz_name:
            tz_obj = tz.gettz(tz_name)
        else:
            tz_obj = tz.gettz()

        now = datetime.now()
        now_tz_time = now.astimezone(tz_obj)
        response_data = {'time': now_tz_time.strftime('%Y-%m-%d %H:%M:%S %z')} 
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response_data).encode('utf-8')]
    except:
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Invalid request\n']

# handle_post_date
def handle_post_date(environ, start_response):
    """
    Handles POST /api/v1/time request: Returns current time in specified timezone (or server's timezone).
    """
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(request_body)
        tz_name = data.get('tz') 

        if tz_name:
            tz_obj = tz.gettz(tz_name)
        else:
            tz_obj = tz.gettz()

        now = datetime.now()
        now_tz_time = now.astimezone(tz_obj)
        response_data = {'time': now_tz_time.strftime('%Y-%m-%d %H:%M:%S %z')} 
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response_data).encode('utf-8')]
    except:
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Invalid request\n']
    
# handle_post_datediff
def handle_post_datediff(environ, start_response):
    """
    Handles POST /api/v1/time request: Returns current time in specified timezone (or server's timezone).
    """
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(request_body)
        tz_name = data.get('tz') 

        if tz_name:
            tz_obj = tz.gettz(tz_name)
        else:
            tz_obj = tz.gettz()

        now = datetime.now()
        now_tz_time = now.astimezone(tz_obj)
        response_data = {'time': now_tz_time.strftime('%Y-%m-%d %H:%M:%S %z')} 
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response_data).encode('utf-8')]
    except:
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Invalid request\n']


# Run the WSGI server
if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()


