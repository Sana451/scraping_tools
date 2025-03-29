import re

import pandas as pd
from scrapy import Selector

# Чтение CSV файла в DataFrame
df = pd.read_csv('/home/sana451/PycharmProjects/scrapy_parsers/schmersal_com/schmersal_com/results/schmersal_com_.de.csv')


def my_function(x):
    # Проверка, что x не пустое и является строкой
    if not x or not isinstance(x, str):
        return ""  # Возвращаем пустое значение, если нет текста

    try:
        # Инициализация селектора для анализа HTML
        sel = Selector(text=x)

        # Вставьте вашу логику извлечения данных здесь
        # Например, если нужно извлечь какое-то значение:
        # result = sel.xpath("(//*[contains(text(), 'eCl@ss Nummer,')])[1]//text()").get(default="").strip()
        result = sel.xpath("(//*[contains(text(), 'eCl@ss Nummer,')])[1]//following-sibling::*//p//text()"
                           ).get(default="").strip()

        return result
    except Exception as e:
        # Обработка исключений, если что-то пошло не так
        print(f"Ошибка при обработке: {e}")
        return ""  # Возвращаем пустое значение в случае ошибки
# def my_function(x):
#     # Инициализация селектора для анализа HTML
#     sel = Selector(text=x)
#
#     #
#
#     # eclass_value = response.xpath(
#     #     "(//*[contains(text(), 'eCl@ss Nummer,')])[1]//following-sibling::*//p//text()").get(default="").strip()
#     # result["eClass value"] = eclass_value
#     result = "qwery"
#     return result

# Применяем функцию к колонке 'A' и создаем новую колонку 'B'
df['eClass value'] = df['Характеристики'].apply(my_function)

# Сохраняем измененный DataFrame в новый CSV файл
df.to_csv('/home/sana451/PycharmProjects/scrapy_parsers/schmersal_com/schmersal_com/results/schmersal_com_.de.csv', index=False)

print("Файл успешно сохранен!")
