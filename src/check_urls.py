import requests

# Establih the proxy connection by finding the correct open tor port using: sudo lsof -i -n -P | grep TCP
proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    }


def access_url(url: str) -> (int, bool, str):
    try:
        data = requests.get(url, proxies=proxies)
        print(f"{data.status_code} from {url}")
        captcha = False
        captcha_type = None
        if "captcha" in str(data.content):
            captcha = True
            captcha_type = "text"
        return data.status_code, captcha, captcha_type
    except Exception as e:
        print(e)
        print(f"error from {url}")
        return 0, None, None
