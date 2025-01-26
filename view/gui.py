import tkinter as tk
from tkinter import ttk, messagebox
from model.db.database import (
    create_database,
    load_contacts_to_list,
    update_contact_in_db,
)
from controller.gui_functions import (
    refresh_contacts,
    delete_contact,
    undo_last_action,
    redo_last_action,
    sort_contacts_by_column,
    search_contacts,
    filter_contacts_by_letter,
    delete_selected_contact,
    reset_search,
)
from view.add_contact_window_gui import *
from view.edit_selected_contact_window_gui import edit_selected_contact


def create_gui():
    create_database()
    contact_list = load_contacts_to_list()

    root = tk.Tk()
    root.title("Menadżer kontaktów")

    # Contacts table
    frame = tk.Frame(root)
    frame.pack(pady=10)

    tree = ttk.Treeview(
        frame,
        columns=("ID", "Imię", "Nazwisko", "Telefon", "Email"),
        show="headings",
    )
    tree.heading(
        "ID",
        text="ID",
        command=lambda: sort_contacts_by_column(
            tree, "contact_id", contact_list
        ),
    )
    tree.heading(
        "Imię",
        text="Imię",
        command=lambda: sort_contacts_by_column(
            tree, "first_name", contact_list
        ),
    )
    tree.heading(
        "Nazwisko",
        text="Nazwisko",
        command=lambda: sort_contacts_by_column(
            tree, "last_name", contact_list
        ),
    )
    tree.heading(
        "Telefon",
        text="Telefon",
        command=lambda: sort_contacts_by_column(
            tree, "phone_number", contact_list
        ),
    )
    tree.heading(
        "Email",
        text="Email",
        command=lambda: sort_contacts_by_column(tree, "email", contact_list),
    )
    tree.pack(side=tk.LEFT)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Dropdown for filtering contacts
    def create_filter_menu(root, tree, contact_list):
        letters = [chr(i) for i in range(65, 91)]  # A-Z
        selected_letter = tk.StringVar()
        selected_letter.set("Wybierz literę")
        filter_menu = tk.OptionMenu(
            root,
            selected_letter,
            *letters,
            command=lambda letter: filter_contacts_by_letter(
                letter, tree, contact_list
            ),
        )
        filter_menu.pack(pady=5)

    # Search field and search + reset button
    search_frame = tk.Frame(root)
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Szukaj:").grid(row=0, column=0)
    entry_search = tk.Entry(search_frame, width=30)
    entry_search.grid(row=0, column=1, padx=5)

    tk.Button(
        search_frame,
        text="Wyszukaj",
        command=lambda: search_contacts(tree, entry_search, contact_list),
    ).grid(row=0, column=2, padx=5)
    tk.Button(
        search_frame,
        text="Resetuj",
        command=lambda: reset_search(tree, entry_search, contact_list),
    ).grid(row=0, column=3, padx=5)

    # Buttons for managing contacts
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Dodaj kontakt",
        command=lambda: add_contact_window(root, tree, contact_list),
    ).grid(row=0, column=0, padx=5)
    tk.Button(
        button_frame,
        text="Usuń kontakt",
        command=lambda: delete_selected_contact(tree, contact_list),
    ).grid(row=0, column=1, padx=5)
    tk.Button(
        button_frame,
        text="Edytuj kontakt",
        command=lambda: edit_selected_contact(root, tree, contact_list),
    ).grid(row=0, column=2, padx=5)
    tk.Button(
        button_frame,
        text="Cofnij zmianę",
        command=lambda: undo_last_action(contact_list, tree),
    ).grid(row=0, column=3, padx=5)
    tk.Button(
        button_frame,
        text="Przywróć zmianę",
        command=lambda: redo_last_action(contact_list, tree),
    ).grid(row=0, column=4, padx=5)

    create_filter_menu(root, tree, contact_list)
    refresh_contacts(tree, contact_list)
    root.mainloop()
