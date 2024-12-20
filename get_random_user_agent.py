import random


def get_random_user_agent():
    """Получаем случайный User-Agent."""
    with open('/home/sana451/PycharmProjects/scrapy_parsers/user-agents.txt', 'r') as file:
        return random.choice(file.readlines()).strip()


def get_random_proxy():
    """Получаем случайный proxy."""
    with open('/home/sana451/PycharmProjects/scrapy_parsers/proxy_1.txt', 'r') as file:
        return random.choice(file.readlines()).strip()


if __name__ == '__main__':
    print(get_random_user_agent())
    print(get_random_proxy())
