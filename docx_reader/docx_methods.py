from aspose.words import Document

from os import remove


def open_docx_file(filepath: str) -> str:
    Document(filepath).save('../app/output.html')
    with open('../app/output.html', 'r', encoding='utf-8') as file:
        text = file.read()
    txt_to_delete = ['Aspose', 'aspose', 'output.001.png']
    for txt in txt_to_delete:
        pos = text.find(txt)
        while pos > -1:
            pos1 = text[:pos].rfind('<')
            pos2 = text.find('>', pos + 1)
            text = text[:pos1] + text[pos2 + 1:]
            pos = text.find(txt)
    with open('../app/output.html', 'w', encoding='utf-8') as file:
        file.write(text)
    return text


def save_docx_file(filepath: str, html_text: str, delete_last_version: bool = False, last_filepath: str = '') -> None:
    with open('output.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_text)
    if delete_last_version:
        remove(last_filepath)
    Document('output.html').save(filepath)
    remove('output.html')
