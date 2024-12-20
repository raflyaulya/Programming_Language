from wsgiref.simple_server import make_server
from datetime import datetime
from dateutil import tz
import json
import requests

# Это WSGI-приложение обрабатывает запросы для предоставления текущего времени
# и расчёта разницы между датами с учетом часовых поясов.

# Определение WSGI-приложения
def application(environ, start_response):
    """
    Основная функция, обрабатывающая все HTTP-запросы, основываясь на пути и методе.
    """
    path = environ['PATH_INFO']  # Извлечение пути из запроса
    method = environ['REQUEST_METHOD']  # Извлечение HTTP-метода

    if path == '/' and method == 'GET':
        # Обработка GET-запроса к /
        return handle_get_root(environ, start_response)
    
    elif path.startswith('/') and method == 'GET':
        # Обработка GET-запроса к /<имя часового пояса>
        return handle_get_timezone(environ, start_response)
    
    elif path == '/api/v1/time' and method == 'POST':
        # Обработка POST-запроса к /api/v1/time
        return handle_post_time(environ, start_response)
    
    elif path == '/api/v1/date' and method == 'POST':
        # Обработка POST-запроса к /api/v1/date
        return handle_post_date(environ, start_response)
    
    elif path == '/api/v1/datediff' and method == 'POST':
        # Обработка POST-запроса к /api/v1/datediff
        return handle_post_datediff(environ, start_response)
    
    else:
        # Обработка неверного запроса
        status = '404 Not Found'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Not Found\n']

# Вспомогательные функции для обработки запросов
def handle_get_root(environ, start_response):
    """
    Возвращает текущее время в часовом поясе сервера в формате HTML.
    """
    now = datetime.now()
    server_tz = tz.gettz()  # Получение часового пояса сервера
    now_server_time = now.astimezone(server_tz)
    html = f"<h1>Текущее время в {server_tz}: {now_server_time.strftime('%Y-%m-%d %H:%M:%S %z')}</h1>"
    status = '200 OK'
    headers = [('Content-Type', 'text/html')]
    start_response(status, headers)
    return [html.encode('utf-8')]

def handle_get_timezone(environ, start_response):
    """
    Возвращает текущее время в указанном часовом поясе.
    """
    try:
        tz_name = environ['PATH_INFO'][1:]  # Извлечение имени часового пояса из пути
        tz_obj = tz.gettz(tz_name)  # Получение объекта часового пояса
        now = datetime.now()
        now_tz_time = now.astimezone(tz_obj)
        html = f"<h1>Текущее время в {tz_name}: {now_tz_time.strftime('%Y-%m-%d %H:%M:%S %z')}</h1>"
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        return [html.encode('utf-8')]
    except:
        # Обработка ошибок при неверном часовом поясе
        status = '404 Not Found'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Invalid timezone\n']

# Обработка POST-запроса к /api/v1/time
def handle_post_time(environ, start_response):
    """
    Возвращает текущее время в формате JSON для указанного часового пояса 
    (или часового пояса сервера, если параметр отсутствует).
    """
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))  # Получение размера тела запроса
        request_body = environ['wsgi.input'].read(request_body_size)  # Чтение данных запроса
        data = json.loads(request_body)  # Разбор JSON
        tz_name = data.get('tz')  # Получение имени часового пояса

        if tz_name:
            tz_obj = tz.gettz(tz_name)  # Получение объекта часового пояса
        else:
            tz_obj = tz.gettz()  # Использование часового пояса сервера

        now = datetime.now()
        now_tz_time = now.astimezone(tz_obj)
        response_data = {'time': now_tz_time.strftime('%Y-%m-%d %H:%M:%S %z')}
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response_data).encode('utf-8')]
    except:
        # Обработка ошибок при некорректном запросе
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Invalid request\n']

# Обработка POST-запроса к /api/v1/date
def handle_post_date(environ, start_response):
    """
    Возвращает текущую дату в формате JSON для указанного часового пояса 
    (или часового пояса сервера, если параметр отсутствует).
    """
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))  # Получение размера тела запроса
        request_body = environ['wsgi.input'].read(request_body_size)  # Чтение данных запроса
        data = json.loads(request_body)  # Разбор JSON
        tz_name = data.get('tz')  # Получение имени часового пояса

        if tz_name:
            tz_obj = tz.gettz(tz_name)  # Получение объекта часового пояса
        else:
            tz_obj = tz.gettz()  # Использование часового пояса сервера

        now = datetime.now()
        now_tz_time = now.astimezone(tz_obj)
        response_data = {'date': now_tz_time.strftime('%Y-%m-%d')}  # Форматирование только даты
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response_data).encode('utf-8')]
    except:
        # Обработка ошибок при некорректном запросе
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Invalid request\n']

# Обработка POST-запроса к /api/v1/datediff
def handle_post_datediff(environ, start_response):
    """
    Рассчитывает разницу между двумя датами, предоставленными в параметрах 'start' и 'end',
    с учетом часового пояса, если он указан.
    """
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))  # Получение размера тела запроса
        request_body = environ['wsgi.input'].read(request_body_size)  # Чтение данных запроса
        data = json.loads(request_body)  # Разбор JSON

        # Извлечение параметров start и end
        start = data.get('start')
        end = data.get('end')

        if not start or not end:
            raise ValueError("Параметры 'start' и 'end' обязательны.")

        # Разбор начальной даты
        start_date = datetime.strptime(start['date'], '%m.%d.%Y %H:%M:%S')
        start_tz = tz.gettz(start.get('tz')) if start.get('tz') else tz.gettz()
        start_date = start_date.replace(tzinfo=start_tz)

        # Разбор конечной даты
        end_date = datetime.strptime(end['date'], '%m.%d.%Y %H:%M:%S')
        end_tz = tz.gettz(end.get('tz')) if end.get('tz') else tz.gettz()
        end_date = end_date.replace(tzinfo=end_tz)

        # Вычисление разницы во времени
        diff = end_date - start_date
        response_data = {'difference': str(diff)}  # Возвращение разницы в виде строки
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response_data).encode('utf-8')]
    except Exception as e:
        # Обработка ошибок при некорректном запросе
        status = '400 Bad Request'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [f'Invalid request: {str(e)}\n'.encode('utf-8')]


# Запуск WSGI-сервера
if __name__ == '__main__':
    """
    Основной блок для запуска сервера. Слушает порт 8000 и обрабатывает входящие запросы.
    """
    with make_server('', 8000, application) as httpd:
        print('Сервер запущен на порту 8000...')
        httpd.serve_forever()
