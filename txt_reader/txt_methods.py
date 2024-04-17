def open_txt_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def save_txt_file(filepath: str, text: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)
