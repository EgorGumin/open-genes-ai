import os
import subprocess
from tqdm import tqdm


def convert_to_pdf(doc_path, soffice_path='soffice'):
    dir_name = os.path.dirname(doc_path)
    subprocess.run([
        soffice_path, '--headless', '--convert-to', 'pdf', '--outdir', dir_name, doc_path
    ], check=True)


def find_doc_files(root_dir):
    doc_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.doc', '.docx')):
                doc_files.append(os.path.join(dirpath, filename))
    return doc_files


def main():
    root_dir = '../../data/supp'
    soffice_path = 'soffice'  # или полный путь к soffice.exe, если не в PATH
    doc_files = find_doc_files(root_dir)
    to_convert = []
    for doc_path in doc_files:
        pdf_name = os.path.splitext(os.path.basename(doc_path))[0] + '.pdf'
        pdf_path = os.path.join(os.path.dirname(doc_path), pdf_name)
        if not os.path.exists(pdf_path):
            to_convert.append(doc_path)
    print(f'Найдено {len(doc_files)} doc/docx файлов, требуется конвертировать: {len(to_convert)}')
    for doc_path in tqdm(to_convert, desc='Конвертация в PDF'):
        try:
            convert_to_pdf(doc_path, soffice_path=soffice_path)
        except Exception as e:
            print(f'Ошибка при конвертации {doc_path}: {e}')


if __name__ == '__main__':
    main() 