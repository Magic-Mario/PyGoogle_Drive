import gspread
from dataclasses import dataclass
from typing import Any, Optional
import pandas as pd
from datetime import date, datetime
from validators.url import url


@dataclass
class Patients:

    # *Authentication variables
    auth = gspread.service_account("Google_Drive/creds.json")


    def authentication(self):
        """Func to authenticate if the received url is valid and related to google spreadsheets"""

        try:
            url_input = "https://docs.google.com/spreadsheets/d/1zRTdhTqTVszV7t-6XkRklj2kXEXAaizp9wOK9FBius8/edit#gid=0"
            if url_input.startswith("https://docs.google.com/spreadsheets/") and url(url_input):
                return self.auth.open_by_url(url_input)

        except Exception:
            print("Inserte un url valido")

    def select_sheet(self, sheet):
        """Func to select which sheet you want to use"""

        title = input("Escribe el nombre de la tabla ha utilizar: ")
        return sheet.worksheet(title)

    def fill_wks(self, wks):
        """Func to find all the cells without a value and fill them with Null value """

        for cell in wks.findall(""):
            if cell.value == "":
                wks.update_cell(cell.row, cell.col, "Null")
        return wks.get_all_values()

    def find_patient(self, wks):
        """Func to check and find if a patient is in the database and return 
        a list with the values in the row"""

        # Patient info
        info = input("Escriba el dato del paciente: ").capitalize()
        for cell in wks.findall(info):
            return wks.row_values(cell.row)  # List with row's info

    def add_patient(self, wks):
        """Func to add a new patient in the database"""
        name = input("Nombre: ").capitalize()
        last_name = input("Apellido: ").capitalize()
        cc = int(input("CC: "))
        email = input("Email: ").lower()
        phone_number = int(input("Numero de contacto: "))
        date = datetime.now()
        init_date = date.strftime("%d-%m-%y")
        row_value = [name, last_name, cc, email,
                     phone_number, init_date]
        return wks.append_row(row_value)

    def update_patient(self, wks):
        """Func to update patients info"""
        patient = self.find_patient(wks)
        cell = wks.find(patient[2])
        cell_list = wks.range(cell.row, 1, cell.row, wks.col_count)

        cell_list[0].value = input(f"Nombre [{cell_list[0].value}]:")
        cell_list[1].value = input(f"Apellido [{cell_list[1].value}]:")
        cell_list[2].value = input(f"CC [{cell_list[2].value}]:")
        cell_list[3].value = input(f"Correo Electrónico [{cell_list[3].value}]:")
        cell_list[4].value = input(f"Numero de teléfono [{cell_list[4].value}]:")

        for index, _ in enumerate(cell_list):
            wks.update_cell(cell_list[index].row, cell_list[index].col, cell_list[index].value)
        return print("Updated")

    def delete_patient(self):
        """Func to remove a patient from the database"""
        pass

    def main(self):
        sheet = self.authentication()
        wks = self.select_sheet(sheet)
        self.fill_wks(wks)
        option = input("Elige una función: ").lower()

        if option == "find":
            return print(self.find_patient(wks))
        elif option == "new":
            return print(self.add_patient(wks))
        elif option == "update":
            return self.update_patient(wks)


if __name__ == '__main__':
    func = Patients()
    func.main()
