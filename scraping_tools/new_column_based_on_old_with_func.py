import re
from scraping_tools.html_clean_tools import del_attrs_from_scrapy_selector

import pandas as pd
from scrapy import Selector

# Чтение CSV файла в DataFrame
df = pd.read_csv(
    '/home/sana451/PycharmProjects/scrapy_parsers/ako_shop_com/ako_shop_com/results/ako_shop_com_.de.csv'
)


def my_function_1(x):
    # Проверка, что x не пустое и является строкой
    if not x or not isinstance(x, str):
        return ""  # Возвращаем пустое значение, если нет текста

    try:
        # Инициализация селектора для анализа HTML
        sel = Selector(text=x, type="html")
        val = sel.xpath("(//span[text()='100']/following::td)[1]/div/text()").get(default="").replace("€*", "").strip()

        return val
    except Exception as e:
        # Обработка исключений, если что-то пошло не так
        print(f"Ошибка при обработке: {e}")
        return ""  # Возвращаем пустое значение в случае ошибки



def my_function_2(x):
    # Проверка, что x не пустое и является строкой
    if not x or not isinstance(x, str):
        return ""  # Возвращаем пустое значение, если нет текста

    try:
        product_num = x.split("/p/")[-1]

        return product_num
    except Exception as e:
        # Обработка исключений, если что-то пошло не так
        print(f"Ошибка при обработке: {e}")
        return ""  # Возвращаем пустое значение в случае ошибки

# my_function(x)
# Применяем функцию к колонке 'A' и создаем новую колонку 'B'
df['price_per_100'] = df['Prices table'].apply(my_function_1)

# # Сохраняем измененный DataFrame в новый CSV файл
df.to_csv(
    '/home/sana451/PycharmProjects/scrapy_parsers/ako_shop_com/ako_shop_com/results/ako_shop_com_.de.csv',
    index=False
)

print("Файл успешно сохранен!")
