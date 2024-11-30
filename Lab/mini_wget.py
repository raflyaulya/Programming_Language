import http.client  # Для выполнения HTTP/HTTPS запросов
import urllib.parse  # Для разбора URL
import sys  # Для работы с аргументами командной строки
import threading  # Для создания отдельного потока для отображения прогресса загрузки
import time  # Для работы с интервалами времени

def download_file(url):
    # Разбираем предоставленный URL на его компоненты (схема, хост, путь и т.д.)
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname  # Доменное имя или IP-адрес
    path = parsed_url.path or "/"  # Путь к файлу; используем "/" по умолчанию, если он отсутствует
    port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)  # Порт по умолчанию для HTTP/HTTPS

    # Создаем HTTP или HTTPS подключение в зависимости от схемы URL
    if parsed_url.scheme == "https":
        conn = http.client.HTTPSConnection(host, port)  # HTTPS соединение
    else:
        conn = http.client.HTTPConnection(host, port)  # HTTP соединение

    # Отправляем HTTP GET запрос на сервер
    headers = {"User-Agent": "Mini-Wget/1.0"}  # Указываем User-Agent для совместимости
    conn.request("GET", path, headers=headers)
    response = conn.getresponse()  # Получаем ответ сервера

    # Обрабатываем перенаправления (коды 301 или 302), следуя новому URL
    if response.status in (301, 302):
        new_url = response.getheader("Location")  # Извлекаем заголовок "Location" с новым URL
        print(f"Перенаправление на: {new_url}")  # Сообщаем пользователю о перенаправлении
        conn.close()  # Закрываем текущее соединение
        return download_file(new_url)  # Рекурсивно вызываем функцию с новым URL

    # Если ответ сервера успешен (код 200), начинаем загрузку файла
    if response.status == 200:
        file_name = path.split("/")[-1] or "downloaded_file"  # Используем последний сегмент пути как имя файла
        print(f"Загрузка файла: {file_name}")

        # Переменные для отслеживания прогресса загрузки
        downloaded_bytes = 0  # Количество загруженных байтов
        total_bytes = response.getheader("Content-Length")  # Общий размер файла (если сервер указал)
        total_bytes = int(total_bytes) if total_bytes else None  # Преобразуем в число, если указано

        # Функция для отображения прогресса загрузки каждую секунду
        def progress_printer():
            while not download_complete:  # Цикл работает, пока загрузка не завершена
                print(f"Загружено: {downloaded_bytes} байт")  # Печатаем количество загруженных байтов
                time.sleep(1)  # Ждем 1 секунду перед следующим обновлением

        # Запускаем отображение прогресса в отдельном потоке
        download_complete = False  # Флаг, указывающий, что загрузка завершена
        progress_thread = threading.Thread(target=progress_printer)  # Создаем поток
        progress_thread.start()  # Запускаем поток

        # Открываем файл для записи бинарных данных
        with open(file_name, "wb") as file:
            # Читаем и записываем файл по частям (по 1024 байта)
            while chunk := response.read(1024):
                file.write(chunk)  # Записываем кусок в файл
                downloaded_bytes += len(chunk)  # Обновляем счетчик загруженных байтов

        # Помечаем загрузку как завершенную и ждем завершения потока прогресса
        download_complete = True
        progress_thread.join()  # Ждем завершения потока
        print(f"Загрузка завершена. Файл сохранен как {file_name}")  # Сообщаем пользователю о завершении

    else:
        # Обрабатываем ошибки (коды ответа, отличные от 200), выводя статус и причину
        print(f"Не удалось загрузить файл: {response.status} {response.reason}")

    # Закрываем HTTP/HTTPS соединение
    conn.close()

if __name__ == "__main__":
    # Проверяем, что скрипт запущен с одним аргументом командной строки
    if len(sys.argv) != 2:
        print("Использование: python mini_wget.py <URL>")  # Инструкция по использованию
        sys.exit(1)  # Завершаем выполнение с кодом ошибки

    # Получаем URL из аргументов командной строки
    url = sys.argv[1]
    # Вызываем функцию для загрузки файла
    download_file(url)

    # an example site to get another example files download: https://filesamples.com/formats/txt 
    # 
    # and also here below another examples:
    # https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3
    # https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png
    # https://via.placeholder.com/150
    # https://filesamples.com/samples/document/txt/sample1.txt
    # https://filesamples.com/samples/document/txt/sample2.txt
    # https://filesamples.com/samples/document/txt/sample3.txt
