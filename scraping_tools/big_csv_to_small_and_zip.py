import csv
import os
import zipfile

def split_csv(input_file, lines_per_file):
    # Получаем путь и имя файла без расширения
    base_path, filename = os.path.split(input_file)
    name, ext = os.path.splitext(filename)

    # Читаем исходный CSV файл
    with open(input_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Читаем заголовок

        # Считаем количество строк
        rows = list(reader)

        # Разбиваем на части
        part_files = []
        for i in range(0, len(rows), lines_per_file):
            part_filename = os.path.join(base_path, f'{name}_part_{i // lines_per_file + 1}{ext}')
            part_files.append(part_filename)

            with open(part_filename, mode='w', newline='', encoding='utf-8') as part_file:
                writer = csv.writer(part_file)
                writer.writerow(header)  # Пишем заголовок
                writer.writerows(rows[i:i + lines_per_file])

    return part_files

def create_zip(files, zip_name):
    # Создаем архив
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))

def main():
    input_file = ''  # Замените на путь к вашему CSV файлу
    lines_per_file = 10000  # Количество строк на файл

    # Разбиваем CSV на части
    part_files = split_csv(input_file, lines_per_file)

    # Создаем архив с разбитыми файлами
    base_path, filename = os.path.split(input_file)
    name, _ = os.path.splitext(filename)
    zip_name = os.path.join(base_path, f'{name}_split_files2.zip')

    create_zip(part_files, zip_name)

    # Удаляем промежуточные файлы
    for part_file in part_files:
        os.remove(part_file)

    print(f"Архив с разбитыми файлами создан: {zip_name}")

if __name__ == '__main__':
    main()
