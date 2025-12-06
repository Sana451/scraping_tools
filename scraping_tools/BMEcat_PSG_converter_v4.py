import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

OUTPUT_FILE = "PSG-catalog_20.11.2025.xml"
CHUNK_SIZE = 50  # Кол-во строк на один процесс


def process_product_chunk(chunk_df):
    articles_xml = []
    for idx, row in chunk_df.iterrows():
        article = ET.Element("ARTICLE")
        ET.SubElement(article, "SUPPLIER_AID").text = str(row['SUPPLIER_AID'])
        article_details = ET.SubElement(article, "ARTICLE_DETAILS")
        ET.SubElement(article_details, "DESCRIPTION_SHORT").text = str(row['DESCRIPTION_SHORT'])
        ET.SubElement(article_details, "DESCRIPTION_LONG").text = str(row['DESCRIPTION_LONG'])
        articles_xml.append(ET.tostring(article, encoding="unicode"))
    return articles_xml


def process_groups(groups_df):
    groups_xml = []
    for _, row in groups_df.iterrows():
        catalog_structure = ET.Element("CATALOG_STRUCTURE", type=str(row['CATALOG_STRUCTURE type']))
        ET.SubElement(catalog_structure, "GROUP_ID").text = str(row['GROUP_ID'])
        ET.SubElement(catalog_structure, "GROUP_NAME").text = str(row['GROUP_NAME'])
        groups_xml.append(ET.tostring(catalog_structure, encoding="unicode"))
    return groups_xml


def write_xml_header(file):
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<BMECAT version="1.2" xmlns="http://www.bmecat.org/bmecat/1.2/bmecat_new_catalog">\n')
    file.write('  <HEADER>\n')
    file.write('    <GENERATOR_INFO>FAMAGA BMEcat Generator for PSG</GENERATOR_INFO>\n')
    file.write('    <CATALOG>\n')
    file.write(f'      <DATETIME type="generation_date"><DATE>{datetime.now().date()}</DATE>'
               f'<TIME>{datetime.now().time().strftime("%H:%M:%S")}</TIME></DATETIME>\n')
    file.write('    </CATALOG>\n')
    file.write('  </HEADER>\n')
    file.write('  <T_NEW_CATALOG>\n')


def write_xml_footer(file):
    file.write('  </T_NEW_CATALOG>\n')
    file.write('</BMECAT>\n')


def read_excel_in_chunks(file_path, sheet_name=0, chunksize=CHUNK_SIZE):
    """Генератор, который возвращает чанки DataFrame из Excel."""
    nrows = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0]).shape[0]
    for start in range(0, nrows, chunksize):
        end = start + chunksize
        chunk = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=range(1, start + 1), nrows=chunksize)
        yield chunk


def main_multiprocess(file_path):
    groups_df = pd.read_excel(file_path, sheet_name=1)
    groups_xml = process_groups(groups_df)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        write_xml_header(f)

        for group_str in groups_xml:
            f.write(group_str + "\n")
        logger.info(f"Группы записаны: {len(groups_xml)}")

        pool = Pool(cpu_count())
        jobs = []

        for chunk in read_excel_in_chunks(file_path, sheet_name=0, chunksize=CHUNK_SIZE):
            job = pool.apply_async(process_product_chunk, args=(chunk,))
            jobs.append(job)

        for job in tqdm(jobs, desc="Обработка чанков продуктов", total=len(jobs)):
            articles_list = job.get()
            for article_str in articles_list:
                f.write(article_str + "\n")

        pool.close()
        pool.join()

        write_xml_footer(f)

    logger.info(f"BMEcat XML успешно создан: {OUTPUT_FILE}")


if __name__ == "__main__":
    main_multiprocess("PSG-catalog_19.11.2025.xlsx")
