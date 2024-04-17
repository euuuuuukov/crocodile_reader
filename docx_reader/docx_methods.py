from aspose.words import Document

from os import remove


def open_docx_file(filepath: str) -> str:
    Document(filepath).save('../app/output.html')
    with open('../app/output.html', 'r', encoding='utf-8') as file:
        text = file.read()
    txt_to_delete = ['<span style="height:0pt; display:block; position:absolute; z-index:-65537"><img src='
                     '"output.001.png" width="624" height="339" alt="" style="margin-top:249.33pt; -aw-left-pos:0pt; '
                     '-aw-rel-hpos:margin; -aw-rel-vpos:margin; -aw-top-pos:0pt; -aw-wrap-type:none; '
                     'position:absolute" /></span>',
                     '<span style="font-weight:bold; color:#ff0000">Evaluation Only. Created with Aspose.Words. '
                     'Copyright 2003-2024 Aspose Pty Ltd.</span>',
                     '<div style="-aw-headerfooter-type:footer-primary; clear:both"><p style="margin-top:0pt; '
                     'margin-bottom:10pt; line-height:115%; font-size:12pt"><span style="font-weight:bold; '
                     'color:#ff0000">Created with an evaluation copy of Aspose.Words. To discover the full versions of '
                     'our APIs please visit: https://products.aspose.com/words/</span></p></div>']
    for txt in txt_to_delete:
        pos = text.find(txt)
        text = text[:pos] + text[pos + len(txt):]
    with open('../app/output.html', 'w', encoding='utf-8') as file:
        file.write(text)
    return text


def save_docx_file(filepath: str, html_text: str, delete_last_version: bool = False, last_filepath: str = '') -> None:
    with open('output.html', 'r', encoding='utf-8') as html_file:
        html_file.write(html_text)
    if delete_last_version:
        remove(last_filepath)
    Document('output.html').save(filepath)
    remove('output.html')
