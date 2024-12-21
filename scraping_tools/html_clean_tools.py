import re
import csv
from types import NoneType

from bs4 import BeautifulSoup
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
