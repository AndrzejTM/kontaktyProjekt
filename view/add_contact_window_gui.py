import tkinter as tk

from assets.gui_parameters import *
from controller.gui_functions import add_contact


# Window for adding new contact
def add_contact_window(root, tree, contact_list):
    add_window = tk.Toplevel(root)
    add_window.title("Dodaj kontakt")
    add_window.minsize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

    tk.Label(add_window, text="Imię").grid(row=0, column=0)
    entry_first_name = tk.Entry(add_window)
    entry_first_name.grid(row=0, column=1)

    tk.Label(add_window, text="Nazwisko").grid(row=1, column=0)
    entry_last_name = tk.Entry(add_window)
    entry_last_name.grid(row=1, column=1)

    tk.Label(add_window, text="Telefon").grid(row=2, column=0)
    entry_phone = tk.Entry(add_window)
    entry_phone.grid(row=2, column=1)

    tk.Label(add_window, text="Email").grid(row=3, column=0)
    entry_email = tk.Entry(add_window)
    entry_email.grid(row=3, column=1)

    tk.Button(
        add_window,
        text="Zapisz",
        command=lambda: add_contact(
            add_window,
            contact_list,
            tree,
            entry_first_name.get(),
            entry_last_name.get(),
            entry_phone.get(),
            entry_email.get(),
        ),
    ).grid(row=4, column=0, columnspan=2)
