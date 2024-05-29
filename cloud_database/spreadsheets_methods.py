from gspread import service_account
from gspread import Cell

from os import remove

from config.app_keys import sheet_info


sheet = service_account(sheet_info['filename']).open_by_key(sheet_info['sheet_key'])
clients = sheet.get_worksheet(0)
errors = sheet.get_worksheet(1)


def check_email(email: str) -> bool:
    cell = clients.find(query=email, in_column=4)
    if cell is None:
        return True
    return False


def do_authentication(name: str, surname: str, email: str, password: str) -> str:
    clients.add_rows(1)
    current_row = clients.row_count
    if current_row == 2:
        index = '1'
    else:
        try:
            index = str(int(clients.cell(current_row - 1, 1).value) + 1)
        except TypeError:
            index = '1'
    clients.update_cells([Cell(current_row, 1, index), Cell(current_row, 2, name),
                          Cell(current_row, 3, surname), Cell(current_row, 4, email),
                          Cell(current_row, 5, password)])
    try:
        remove('../app_database/is_authenticated.txt')
    except FileNotFoundError:
        pass
    return index


def do_sign_in(email: str, password: str) -> str:
    query = clients.find(query=email, in_column=4)
    if query is None:
        return 'Неправильный e-mail или пароль'
    if clients.cell(query.row, 5).value == password:
        return str(clients.cell(query.row, 1).value)
    return 'Неправильный e-mail или пароль'


def get_user_data(index: str) -> list[str]:
    current_row = clients.find(query=index, in_column=1).row
    return [clients.cell(current_row, i).value for i in range(1, 6)]


def rewrite_user_info(index: str, name: str, surname: str, password: str) -> None:
    current_row = clients.find(query=index, in_column=1).row
    clients.update_cells([Cell(current_row, 2, name), Cell(current_row, 3, surname),
                          Cell(current_row, 5, password)])


def write_bug_report(error: str, actions: str, contact_email: str) -> None:
    errors.add_rows(1)
    current_row = errors.row_count
    with open('../app_database/log.log', 'r', encoding='utf-8') as logs:
        errors.update_cells([Cell(current_row, 1, error), Cell(current_row, 2, actions),
                             Cell(current_row, 3, contact_email), Cell(current_row, 4, logs.read()),
                             Cell(current_row, 5, '-')])
