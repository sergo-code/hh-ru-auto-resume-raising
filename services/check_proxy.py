import requests


def is_valid(proxy) -> bool:
    url = 'https://8.8.8.8/'
    try:
        requests.head(url, proxies={'https': proxy})
        return True
    except requests.exceptions.ProxyError:
        return False


if __name__ == '__main__':
    from services.env import Config

    print(is_valid({'https': Config.proxy}))
