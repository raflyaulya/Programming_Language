import http.client
import urllib.parse
import sys

def download_file(url):
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path or "/"
    port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)

    # Koneksi HTTP/HTTPS
    if parsed_url.scheme == "https":
        conn = http.client.HTTPSConnection(host, port)
    else:
        conn = http.client.HTTPConnection(host, port)

    # Kirim permintaan GET
    headers = {"User-Agent": "Mini-Wget/1.0"}
    conn.request("GET", path, headers=headers)
    response = conn.getresponse()

    # Tangani Redirect
    if response.status in (301, 302):  # Redirect
        new_url = response.getheader("Location")
        print(f"Redirected to: {new_url}")
        conn.close()
        return download_file(new_url)

    # Cek jika respon sukses
    if response.status == 200:
        file_name = path.split("/")[-1] or "downloaded_file"
        print(f"Downloading file: {file_name}")

        with open(file_name, "wb") as file:
            while chunk := response.read(1024):
                file.write(chunk)
        print(f"File downloaded successfully: {file_name}")
    else:
        print(f"Failed to download file: {response.status} {response.reason}")

    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mini_wget.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    download_file(url)
