from gspread import service_account
from gspread import Cell

from config.keys import sheet_info


sheet = service_account(sheet_info['filename']).open_by_key(sheet_info['sheet_key'])
clients = sheet.get_worksheet(0)


def check_email(email: str) -> bool:
    cell = clients.find(query=email, in_column=3)
    if cell is None:
        return True
    return False


def do_authentication(name: str, surname: str, email: str, password: str) -> None:
    clients.add_rows(1)
    clients.update_cells([Cell(clients.row_count, 2, name), Cell(clients.row_count, 3, surname),
                          Cell(clients.row_count, 4, email), Cell(clients.row_count, 5, password)])
    if clients.row_count == 2:
        clients.update_cell(2, 1, 1)
    else:
        clients.update_cell(clients.row_count, 1, int(clients.cell(clients.row_count - 1, 1).value) + 1)


def do_sign_in(email: str, password: str) -> bool:
    query = clients.find(query=email, in_column=4)
    if query is None:
        return False
    if clients.cell(query.row, 5).value == password:
        return True
    return False
