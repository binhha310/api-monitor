import requests, socket

def check_http(url, timeout):
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code, r.elapsed.total_seconds()
    except Exception as e:
        return None, str(e)

def check_tcp(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, None
    except Exception as e:
        return False, str(e)
