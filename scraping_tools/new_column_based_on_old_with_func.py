import re
from scraping_tools.html_clean_tools import del_attrs_from_scrapy_selector

import pandas as pd
from scrapy import Selector

# Чтение CSV файла в DataFrame
df = pd.read_csv(
    '/home/sana451/PycharmProjects/scrapy_parsers/de_rubix_com/de_rubix_com/results/de_rubix_com..de.3.csv'
)


def my_function(x):
    # Проверка, что x не пустое и является строкой
    if not x or not isinstance(x, str):
        return ""  # Возвращаем пустое значение, если нет текста

    try:
        # Инициализация селектора для анализа HTML
        sel = Selector(text=x, type="html")

        root = sel.root

        res = []

        for node in root.iter():
            if node.tag == "b":
                print(node.xpath("./text()"))
                print(type(node.xpath("./text()")))
                # res.append(node.xpath("./text()").get(default="").strip())
            if  node.tag == "br":
                res.append("\n")
            # if node.text and node.text.strip():
            #     res.append((node.text.strip(), node.tag))  # текст внутри тега

            # if node.tail and node.tail.strip():
            #     parent = node.getparent()
            #     if parent is not None:
            #         res.append((node.tail.strip(), parent.tag))  # текст между тегами принадлежит родителю
            #     else:
            #         res.append((node.tail.strip(), None))  # если родителя нет (редко)

        # val = sel.xpath("//tr[contains(., 'Verp.-einheit')]//td[2]//text()").get(default="").strip()
        val = "".join(res)


        return val
    except Exception as e:
        # Обработка исключений, если что-то пошло не так
        print(f"Ошибка при обработке: {e}")
        return ""  # Возвращаем пустое значение в случае ошибки


# my_function(x)
# Применяем функцию к колонке 'A' и создаем новую колонку 'B'
df['ECLASS name'] = df['Характеристики'].apply(my_function)

# # Сохраняем измененный DataFrame в новый CSV файл
df.to_csv(
    '/home/sana451/PycharmProjects/scrapy_parsers/de_rubix_com/de_rubix_com/results/de_rubix_com.all.de.csv',
    index=False
)

print("Файл успешно сохранен!")
