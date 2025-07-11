import csv
import re
from lxml import html
from types import NoneType
from typing import Union

from bs4 import BeautifulSoup
from scrapy.selector import Selector, SelectorList
from tabulate import tabulate


def save_error(url, error, field, err_file_path):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


def del_classes_AND_divs_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    [d.decompose() for d in soup.find_all("div")]

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name", "aria-label", "role", "colspan"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def del_classes_from_html(html) -> str:
    if type(html) is NoneType:
        return ""
    if not isinstance(html, BeautifulSoup):
        soup = BeautifulSoup(html, "html.parser")
    else:
        soup = html
    for tag in soup():
        for attribute in [
            "class", "style", "id", "scope", "data-th", "data-table", "data-tbody",
            "data-cell", "border", "rowspan", "data-mce-selected",
            "target", "itemprop", "content", "data-description", "data-uid", "draggable",
            "data-name", "href", "title", "cellpadding", "cellspacing", "width",
            "colspan", "data-target", "role", "data-toggle", "aria-controls", "data-action",
            "aria-selected", "aria-describedby", "data-testid", "version", "data-remise", "min",
            "xmlns", "xlink:href", "type", "src", "srcset", "sizes", "data-nimg", "data-produit",
            "decoding", "alt", "height", "loading", "data-label", "data-link", "value",
            "data-declinaison", "data-mce-style", "align", "valign", "currentitem", "data-for",
            "data-tip", ""
        ]:
            del tag[attribute]

        for s in soup.select("svg"):
            s.extract()
        for s in soup.select("input"):
            s.extract()
        for s in soup.select("button"):
            s.extract()

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(["class", "style", "id", "scope", "data-th", "target", "svg", "use"]):
        data.decompose()

    return ' '.join(soup.stripped_strings)


def create_html_table(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    res = []
    divs = soup.find_all("div")
    for div in divs:
        span_list = div.find_all("span")
        if len(span_list) == 2:
            res.append(i.text.strip() for i in span_list)

    html = tabulate(res, tablefmt="html").replace("\n", "")

    return html


def get_value_from_json_by_value(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = get_value_from_json_by_value(v, key)
            if item is not None:
                return item


def remove_html_comments(html_str: str) -> str:
    """Удаляет все HTML-комментарии из строки с базовой защитой от ошибок."""
    if not isinstance(html_str, str):
        return ""
    try:
        return re.sub(r"<!--.*?-->", "", html_str, flags=re.DOTALL)
    except re.error as e:
        print(f"[Ошибка регулярки]: {e}")
        return html_str


def del_attrs_from_scrapy_selector(selector: Union[Selector, SelectorList]) -> str:
    selector_content = selector.get()
    if selector_content is None:
        return ""

    selector_content = remove_html_comments(selector_content)  # удаляем комментарии

    tree = html.fromstring(selector_content)
    for element in tree.iter():
        for attribute in list(element.attrib):
            del element.attrib[attribute]
    cleaned_str = html.tostring(tree, pretty_print=True).decode()
    return cleaned_str
