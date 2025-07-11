import requests

# Временно — для проверки IP через прокси
test_url = "https://httpbin.org/ip"

with open("/home/sana451/PycharmProjects/scrapy_parsers/proxy.txt", "r", encoding="utf-8") as f:
    proxy_list = f.readlines()

for proxy in proxy_list:
    proxy = proxy.strip()

    if proxy.count(":") == 3:
        ip, port, user, pwd = proxy.split(":")
        proxy_ip = ip  # IP из прокси строки
        proxy_url = f"http://{user}:{pwd}@{ip}:{port}"
    else:
        proxy_ip = proxy.split(":")[0]
        proxy_url = f"http://{proxy}"

    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        response_ip = response.json()["origin"]

        if proxy_ip in response_ip:
            print(f"✅ Proxy {proxies} is working as expected: {proxy_ip} == {response_ip}")
        else:
            print(f"⚠️  Proxy mismatch: {proxy_ip} != {response_ip}")
    except Exception as e:
        print(f"❌ Proxy is dead: {proxy}")
        print("Error:", e)


