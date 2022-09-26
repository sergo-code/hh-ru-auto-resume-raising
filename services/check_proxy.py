import requests


def is_valid(proxy) -> bool:
    url = 'https://8.8.8.8/'
    try:
        requests.head(url, proxies={'https': proxy})
        return True
    except requests.exceptions.ProxyError: #  or AttributeError
        return False


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()
    print(is_valid({'https': os.getenv('proxy')}))
