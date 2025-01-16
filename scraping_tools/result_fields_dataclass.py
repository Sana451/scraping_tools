from dataclasses import dataclass


@dataclass
class ResultFields:
    url: str = "url"
    base_url: str = "base_url"
    title: str = "Заголовок"
    article: str = "Артикул"
    availability: str = "Доступность"
    delivery: str = "Доставка"
    shipment: str = "Поставка"
    ean: str = "ean"
    mpn: str = "mpn"
    gtin: str = "gtin"
    sku: str = "sku"
    manufacturer: str = "Производитель"
    categories: str = "Категории"
    price: str = "Цена"
    discounted_price: str = "Цена со скидкой"
    price_without_discount: str = "Цена без скидки"
    stock: str = "Наличие"
    images: str = "Изображения"
    pdf: str = "pdf"
    weight: str = "Вес"
    short_description: str = "Краткое описание"
    description: str = "Описание"
    details: str = "Характеристики"
    parsing_date: str = "Дата парсинга"
