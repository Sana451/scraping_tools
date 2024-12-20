from http.cookies import SimpleCookie

def cookie_dict_from_string(raw_cookie_str: str) -> dict:
    cookie = SimpleCookie()
    cookie.load(raw_cookie_str)
    cookies = {k: v.value for k, v in cookie.items()}
    return cookies
