import streamlit as st
import re
import os
from datetime import datetime
from urllib.request import urlopen, Request
from openpyxl import Workbook
from bs4 import BeautifulSoup

save_excel = True  # Cambiar a "True" para guardar el correo electrónico en Excel
book = Workbook()
sheet = book.active

def start_scrape(page, name_the_file):

    st.write("\n\nLa página web se está raspando actualmente... por favor espera...")

    scrape = BeautifulSoup(page, 'html.parser')
    scrape = scrape.get_text()

    phone_numbers = set(re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})", scrape))
    emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", scrape))

    nodupnumber = len(list(phone_numbers))
    nodupemail = len(list(emails))

    dupnumber = len(list(re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})", scrape)))
    dupemail = len(list(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", scrape)))

    number_of_dup_number = int(dupnumber) - int(nodupnumber)
    number_of_dup_email = int(dupemail) - int(nodupemail)

    email_list = list(emails)

    if len(phone_numbers) == 0:
        st.write("No se encontraron número(s) de teléfono.")
        st.write("-----------------------------\n")
    else:
        count = 1
        for item in phone_numbers:
            st.write("Número de teléfono #" + str(count) + ': ' + item)
            count += 1

    st.write("-----------------------------\n")

    if len(emails) == 0:
        st.write("No se encontraron dirección(es) de correo electrónico.")
        st.write("-----------------------------\n")
    else:
        count = 1
        for item in emails:
            st.write('Dirección de correo electrónico #' + str(count) + ': ' + item)
            count += 1

    if save_excel:
        for row in zip(email_list):
            sheet.append(row)
        excel_file = (name_the_file + ".xlsx")
        book.save(excel_file)

    st.write("\nSe han eliminado los duplicados de la lista.")
    st.write("Total de números de teléfono: ", nodupnumber)
    st.write("Total de direcciones de correo electrónico: ", nodupemail)
    st.write("Hubo " + str(number_of_dup_number) + " números de teléfono duplicados.")
    st.write("Hubo " + str(number_of_dup_email) + " direcciones de correo electrónico duplicadas.")

    if save_excel:
        st.write("\n\nLos datos se han almacenado en una hoja de cálculo de Excel llamada: "
                 + excel_file + " en este directorio: " + os.getcwd())
        mod_time = os.stat(excel_file).st_mtime
        st.write("\nCompletado a las: " + str(datetime.fromtimestamp(mod_time)))
        st.write("\nTamaño del archivo: " + str(os.stat(excel_file).st_size) + " KB")

def main():

    webpage = st.text_input("Pegue la página web que le gustaría raspar (incluya http/https): ")

    if save_excel:
        name_the_file = st.text_input("Nombre del archivo en el que le gustaría guardar los datos (no incluya .xlsx): ")

    if st.button("Raspar"):
        if not webpage.startswith('http://') and not webpage.startswith('https://'):
            st.write("La URL debe comenzar con 'http://' o 'https://'")
            return

        try:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(webpage, headers=hdr)
            page = urlopen(req)
            start_scrape(page, name_the_file)
        except Exception as e:
            st.write(f"No se pudo abrir la URL: {str(e)}")

if __name__ == "__main__":
    main()
