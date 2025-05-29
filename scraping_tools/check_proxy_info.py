import requests

url = "http://ip-api.com/json"
resp = requests.get(
    url,
    proxies={
        'http': 'http://3kYPYt:NQ1HG8@191.102.148.218:9033',
        'https': 'http://3kYPYt:NQ1HG8@191.102.148.218:9033',
    }
)

if resp.status_code == 200:
    geo_data = resp.json()

    print("Геолокация:")
    print("-" * 30)
    print(f"Статус: {geo_data.get('status', '')}")
    print(f"Страна: {geo_data.get('country', '')}")
    print(f"Регион: {geo_data.get('regionName', '')}")
    print(f"Город: {geo_data.get('city', '')}")
    print(f"Почтовый индекс: {geo_data.get('zip', '')}")
    print(f"Часовой пояс: {geo_data.get('timezone', '')}")
    print("-" * 30)
else:
    print(resp.status_code)
