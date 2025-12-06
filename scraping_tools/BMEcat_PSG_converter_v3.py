import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def read_excel(file_path, test_mode=False, nrows=20):
    """Чтение данных из XLSX файла."""
    logger.info(f"Чтение данных из файла: {file_path}")
    try:
        # Ограничиваем количество строк, если включен тестовый режим
        df_products = pd.read_excel(file_path, sheet_name=0, nrows=nrows if test_mode else None)
        df_groups = pd.read_excel(file_path, sheet_name=1, nrows=nrows if test_mode else None)
        logger.info(
            f"Данные успешно загружены: {len(df_products)} продуктов, {len(df_groups)} групп."
        )
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла: {str(e)}")
        raise
    return df_products, df_groups


def create_bmecat_xml(products_df, groups_df, output_file="PSG-catalog_20.11.2025.xml"):
    """Создание BMEcat XML из DataFrame."""
    # Корневой элемент
    bmecat = ET.Element("BMECAT", version="1.2", xmlns="http://www.bmecat.org/bmecat/1.2/bmecat_new_catalog")

    article_to_cataloggroup_list = []

    # HEADER
    header = ET.SubElement(bmecat, "HEADER")
    generator_info = ET.SubElement(header, "GENERATOR_INFO")
    generator_info.text = "FAMAGA BMEcat Generator for PSG"

    catalog = ET.SubElement(header, "CATALOG")
    ET.SubElement(catalog, "LANGUAGE").text = "de"
    ET.SubElement(catalog, "CATALOG_ID").text = "FAMAGA_2025_1"
    ET.SubElement(catalog, "CATALOG_VERSION").text = "1"
    ET.SubElement(catalog, "CATALOG_NAME").text = "FAMAGA Product Catalog"

    datetime_elem = ET.SubElement(catalog, "DATETIME", type="generation_date")
    ET.SubElement(datetime_elem, "DATE").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(datetime_elem, "TIME").text = datetime.now().strftime("%H:%M:%S")
    ET.SubElement(catalog, "TIMEZONE").text = "+02:00"

    ET.SubElement(catalog, "CURRENCY").text = "EUR"
    ET.SubElement(catalog, "MIME_ROOT").text = "/catalog/media/"

    supplier = ET.SubElement(header, "BUYER")
    ET.SubElement(supplier, "BUYER_NAME").text = "PSG"
    ET.SubElement(supplier, "BUYER_ID", type="buyer").text = "PSG"

    supplier = ET.SubElement(header, "SUPPLIER")
    ET.SubElement(supplier, "SUPPLIER_NAME").text = "FAMAGA GROUP GmbH & Co. KG"
    ET.SubElement(supplier, "SUPPLIER_ID", type="supplier").text = "FAMAGA GROUP GmbH & Co. KG"

    # T_NEW_CATALOG
    t_new_catalog = ET.SubElement(bmecat, "T_NEW_CATALOG")

    # CATALOG_GROUP_SYSTEM
    catalog_group_system = ET.SubElement(t_new_catalog, "CATALOG_GROUP_SYSTEM")

    # Добавление групп
    for _, row in groups_df.iterrows():
        group_id = str(row['GROUP_ID'])
        group_name = str(row['GROUP_NAME'])
        group_type = str(row['CATALOG_STRUCTURE type'])
        parent_id = str(row['PARENT_ID']) if pd.notna(row['PARENT_ID']) else None

        catalog_structure = ET.SubElement(catalog_group_system, "CATALOG_STRUCTURE", type=group_type)
        ET.SubElement(catalog_structure, "GROUP_ID").text = group_id
        ET.SubElement(catalog_structure, "GROUP_NAME").text = group_name
        if parent_id:
            ET.SubElement(catalog_structure, "PARENT_ID").text = parent_id
        if pd.notna(row['GROUP_ORDER']):
            ET.SubElement(catalog_structure, "GROUP_ORDER").text = str(int(row['GROUP_ORDER']))
        if pd.notna(row['GROUP_DESCRIPTION']):
            ET.SubElement(catalog_structure, "GROUP_DESCRIPTION").text = str(row['GROUP_DESCRIPTION'])

        # Обработка MIME для групп
        mime_source = row.get('MIME_SOURCE')
        mime_purpose = row.get('MIME_PURPOSE')
        mime_type = row.get('MIME_Type', 'image/jpeg')  # Значение по умолчанию
        print(f"Группа {group_id}: MIME type={mime_type}, source={mime_source}, purpose={mime_purpose}")
        if pd.notna(mime_source) and pd.notna(mime_purpose):
            mime_info = ET.SubElement(catalog_structure, "MIME_INFO")
            mime = ET.SubElement(mime_info, "MIME")
            ET.SubElement(mime, "MIME_TYPE").text = str(mime_type)
            ET.SubElement(mime, "MIME_SOURCE").text = (mime_source)
            ET.SubElement(mime, "MIME_PURPOSE").text = str(mime_purpose)

    # Добавление продуктов
    for idx, row in products_df.iterrows():
        article = ET.SubElement(t_new_catalog, "ARTICLE")

        # Основные данные
        ET.SubElement(article, "SUPPLIER_AID").text = str(row['SUPPLIER_AID'])

        article_details = ET.SubElement(article, "ARTICLE_DETAILS")
        ET.SubElement(article_details, "DESCRIPTION_SHORT").text = str(row['DESCRIPTION_SHORT'])
        ET.SubElement(article_details, "DESCRIPTION_LONG").text = str(row['DESCRIPTION_LONG'])
        # Исправление EAN: только числовое значение
        ean_value = row.get('EAN', '')
        if pd.notna(ean_value) and ean_value != '':
            try:
                ean_value = str(int(float(ean_value)))
            except (ValueError, TypeError):
                ean_value = str(ean_value)
        else:
            ean_value = ""
        ET.SubElement(article_details, "EAN").text = ean_value
        ET.SubElement(article_details, "MANUFACTURER_NAME").text = str(row['MANUFACTURER_NAME'])
        ET.SubElement(article_details, "MANUFACTURER_AID").text = str(row['MANUFACTURER_AID'])
        if pd.notna(row['DELIVERY_TIME']):
            ET.SubElement(article_details, "DELIVERY_TIME").text = str(int(row['DELIVERY_TIME']))

        # Ключевые слова
        if pd.notna(row['KEYWORD']):
            for keyword in str(row['KEYWORD']).split(','):
                ET.SubElement(article_details, "KEYWORD").text = keyword.strip()

        if pd.notna(row['ARTICLE_ORDER']):
            ET.SubElement(article_details, "ARTICLE_ORDER").text = str(int(row['ARTICLE_ORDER']))



        # Характеристики
        article_features = ET.SubElement(article, "ARTICLE_FEATURES")

        # Добавление REFERENCE_FEATURE_SYSTEM_NAME и REFERENCE_FEATURE_GROUP_ID
        ref_system_name = row.get('REFERENCE_FEATURE_SYSTEM_NAME')
        ref_group_id = row.get('REFERENCE_FEATURE_GROUP_ID')
        if pd.notna(ref_system_name) and pd.notna(ref_group_id):
            ET.SubElement(article_features, "REFERENCE_FEATURE_SYSTEM_NAME").text = str(ref_system_name)
            ET.SubElement(article_features, "REFERENCE_FEATURE_GROUP_ID").text = str(ref_group_id)

        for i in range(1, 11):
            fname = row.get(f'FNAME{i}')
            fvalue = row.get(f'FVALUE{i}')
            funit = row.get(f'FUNIT{i}')
            if pd.notna(fname) and pd.notna(fvalue):
                feature = ET.SubElement(article_features, "FEATURE")
                ET.SubElement(feature, "FNAME").text = str(fname)
                ET.SubElement(feature, "FVALUE").text = str(fvalue)
                if pd.notna(funit):
                    ET.SubElement(feature, "FUNIT").text = str(funit)

        # Условия заказа
        article_order_details = ET.SubElement(article, "ARTICLE_ORDER_DETAILS")
        if pd.notna(row['ORDER_UNIT']):
            ET.SubElement(article_order_details, "ORDER_UNIT").text = str(row['ORDER_UNIT'])
        if pd.notna(row['CONTENT_UNIT']):
            ET.SubElement(article_order_details, "CONTENT_UNIT").text = str(row['CONTENT_UNIT'])
        if pd.notna(row['NO_CU_PER_OU']):
            ET.SubElement(article_order_details, "NO_CU_PER_OU").text = str(int(row['NO_CU_PER_OU']))
        if pd.notna(row['PRICE_QUANTITY']):
            ET.SubElement(article_order_details, "PRICE_QUANTITY").text = str(int(row['PRICE_QUANTITY']))
        if pd.notna(row['QUANTITY_MIN']):
            ET.SubElement(article_order_details, "QUANTITY_MIN").text = str(int(row['QUANTITY_MIN']))
        if pd.notna(row['QUANTITY_INTERVAL']):
            ET.SubElement(article_order_details, "QUANTITY_INTERVAL").text = str(int(row['QUANTITY_INTERVAL']))

        # Цены
        article_price_details = ET.SubElement(article, "ARTICLE_PRICE_DETAILS")
        article_price = ET.SubElement(article_price_details, "ARTICLE_PRICE", price_type=str(row['PRICE_1_price_type']))
        ET.SubElement(article_price, "PRICE_AMOUNT").text = str(row['PRICE_1_PRICE_AMOUNT'])
        ET.SubElement(article_price, "PRICE_CURRENCY").text = str(row['PRICE_1_PRICE_CURRENCY'])
        ET.SubElement(article_price, "TAX").text = str(row['PRICE_1_TAX'])
        ET.SubElement(article_price, "LOWER_BOUND").text = "1"
        if pd.notna(row['PRICE_1_TERRITORY']):
            ET.SubElement(article_price, "TERRITORY").text = str(row['PRICE_1_TERRITORY'])
        if pd.notna(row['PRICE_1_VALID_START_DATE']):
            datetime_price = ET.SubElement(article_price, "DATETIME", type="valid_start_date")
            ET.SubElement(datetime_price, "DATE").text = str(row['PRICE_1_VALID_START_DATE'])[:10]
        if pd.notna(row['PRICE_1_VALID_END_DATE']):
            datetime_price = ET.SubElement(article_price, "DATETIME", type="valid_end_date")
            ET.SubElement(datetime_price, "DATE").text = str(row['PRICE_1_VALID_END_DATE'])[:10]

        # MIME_INFO
        mime_added = False
        mime_info = None
        print(f"Продукт {row['SUPPLIER_AID']}:")
        for i in range(8):
            # Исправление обработки столбцов для i=0
            mime_type_col = 'MIME_Type0' if i == 0 else f'MIME_Type{i}'
            mime_source_col = 'MIME_SOURCE0' if i == 0 else f'MIME_SOURCE{i}'
            mime_purpose_col = 'MIME_PURPOSE0' if i == 0 else f'MIME_PURPOSE{i}'
            mime_descr_col = f'MIME_DESCR{i + 1}' if i > 0 else 'MIME_DESCR1'

            mime_type = row.get(mime_type_col)
            mime_source = row.get(mime_source_col)
            mime_purpose = row.get(mime_purpose_col)
            mime_descr = row.get(mime_descr_col)

            # Исправление некорректных MIME_Type
            if pd.notna(mime_type) and str(mime_type).strip().lower() == 'normal':
                mime_type = 'image/jpeg'
                mime_purpose = 'normal' if not pd.notna(mime_purpose) else mime_purpose

            print(f"  MIME{i}: type={mime_type}, source={mime_source}, purpose={mime_purpose}, descr={mime_descr}")
            # Проверка на валидность всех трёх полей
            if pd.notna(mime_type) and pd.notna(mime_source) and pd.notna(mime_purpose):
                if not mime_added:
                    mime_info = ET.SubElement(article, "MIME_INFO")
                    mime_added = True
                mime = ET.SubElement(mime_info, "MIME")
                ET.SubElement(mime, "MIME_TYPE").text = str(mime_type).strip()
                ET.SubElement(mime, "MIME_SOURCE").text = str(mime_source).strip()
                ET.SubElement(mime, "MIME_PURPOSE").text = str(mime_purpose).strip()
                if pd.notna(mime_descr):
                    ET.SubElement(mime, "MIME_DESCR").text = str(mime_descr).strip()

        # ARTICLE_TO_CATALOGGROUP_MAP
        if pd.notna(row['CATALOG_GROUP_ID']):
            article_to_cataloggroup_list.append({
                "SUPPLIER_AID": str(row['SUPPLIER_AID']),
                "CATALOG_GROUP_ID": str(row['CATALOG_GROUP_ID']),
                "ARTICLE_TO_CATALOGGROUP_MAP_ORDER": str(idx + 1)
            })

        # ARTICLE_REFERENCE
        for ref_type in ['similar', 'accessories', 'others']:
            ref_value = row.get(f'ARTICLE_REFERENCE type={ref_type}')
            if pd.notna(ref_value):
                article_ref = ET.SubElement(article, "ARTICLE_REFERENCE", type=ref_type)
                ET.SubElement(article_ref, "ART_ID_TO").text = str(ref_value)

        # BUYER_AID
        buyer_aid_type = row.get('BUYER_AID type')
        buyer_aid = row.get('BUYER_AID')
        if pd.notna(buyer_aid_type) and pd.notna(buyer_aid):
            ET.SubElement(article, "BUYER_AID", type=str(buyer_aid_type)).text = str(buyer_aid)

        # ERP_GROUP_BUYER
        if pd.notna(row['ERP_GROUP_BUYER']):
            ET.SubElement(article, "ERP_GROUP_ID").text = str(row['ERP_GROUP_BUYER'])

        # SPECIAL_TREATMENT_CLASS
        # if pd.notna(row['SPECIAL_TREATMENT_CLASS']):
        #     ET.SubElement(article, "SPECIAL_TREATMENT_CLASS").text = str(row['SPECIAL_TREATMENT_CLASS'])

    for item in article_to_cataloggroup_list:
        atcg = ET.SubElement(t_new_catalog, "ARTICLE_TO_CATALOGGROUP_MAP")
        ET.SubElement(atcg, "SUPPLIER_AID").text = item["SUPPLIER_AID"]
        ET.SubElement(atcg, "CATALOG_GROUP_ID").text = item["CATALOG_GROUP_ID"]
        ET.SubElement(atcg, "ARTICLE_TO_CATALOGGROUP_MAP_ORDER").text = item["ARTICLE_TO_CATALOGGROUP_MAP_ORDER"]

    # Форматирование и сохранение XML
    xml_str = minidom.parseString(ET.tostring(bmecat, encoding='unicode')).toprettyxml(indent="    ")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_str)
    return xml_str


def main(test_mode=False):
    file_path = "PSG-catalog_19.11.2025.xlsx"  # Укажите путь к вашему файлу
    try:
        products_df, groups_df = read_excel(file_path, test_mode=test_mode)
        create_bmecat_xml(products_df, groups_df)
        logger.info(f"BMEcat XML успешно создан: {file_path.replace('.xlsx', '.xml')}")
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    # main(test_mode=True)  # Для теста ограничим 20 строками
    main(test_mode=False)  # Для полноценного запуска с полным файлом