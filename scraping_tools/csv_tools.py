import csv
import pandas as pd

def read_column_from_csv_file(path: str, column_name: str) -> list:
    """
    Читает указанный столбец по названию из CSV-файла.

    :param path: Путь к CSV-файлу.
    :param column_name: Название столбца, который нужно извлечь.
    :return: Список значений из указанного столбца.
    :raises ValueError: Если указанный столбец не найден.
    """
    df = pd.read_csv(path, encoding="utf-8")
    if column_name not in df.columns:
        raise ValueError(f"Столбец '{column_name}' не найден в файле.")
    return df[column_name].tolist()


def read_row_from_csv_file(path: str, num: int = 0) -> list:
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        return [row[num] for row in list(reader)[1:]]