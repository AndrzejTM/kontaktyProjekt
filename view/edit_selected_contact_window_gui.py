import tkinter as tk


# Logic for editing selected contact
from tkinter import messagebox

from controller.gui_functions import refresh_contacts
from model.db.database import update_contact_in_db


def edit_selected_contact(root, tree, contact_list):
    print("EDIT CONTACT WINDOW")
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Błąd", "Nie wybrano kontaktu do edycji.")
        return

    contact_id = int(selected_item)
    current = contact_list.head
    while current:
        if current.contact_id == contact_id:
            break
        current = current.next

    if not current:
        messagebox.showerror("Błąd", "Nie znaleziono kontaktu.")
        return

    def save_edited_contact():
        new_first_name = entry_first_name.get()
        new_last_name = entry_last_name.get()
        new_phone_number = entry_phone.get()
        new_email = entry_email.get()

        if not new_first_name or not new_last_name or not new_phone_number:
            messagebox.showerror(
                "Błąd", "Wszystkie pola oprócz email są wymagane."
            )
            return

        # Update in DB
        update_contact_in_db(
            contact_id,
            new_first_name,
            new_last_name,
            new_phone_number,
            new_email,
        )

        # Update in the list
        current.first_name = new_first_name
        current.last_name = new_last_name
        current.phone_number = new_phone_number
        current.email = new_email

        refresh_contacts(tree, contact_list)
        edit_window.destroy()
        messagebox.showinfo("Sukces", "Kontakt został zaktualizowany.")

    # Edit contact window
    edit_window = tk.Toplevel(root)
    edit_window.title("Edytuj kontakt")

    tk.Label(edit_window, text="Imię").grid(row=0, column=0)
    entry_first_name = tk.Entry(edit_window)
    entry_first_name.grid(row=0, column=1)
    entry_first_name.insert(0, current.first_name)

    tk.Label(edit_window, text="Nazwisko").grid(row=1, column=0)
    entry_last_name = tk.Entry(edit_window)
    entry_last_name.grid(row=1, column=1)
    entry_last_name.insert(0, current.last_name)

    tk.Label(edit_window, text="Numer telefonu").grid(row=2, column=0)
    entry_phone = tk.Entry(edit_window)
    entry_phone.grid(row=2, column=1)
    entry_phone.insert(0, current.phone_number)

    tk.Label(edit_window, text="Email").grid(row=3, column=0)
    entry_email = tk.Entry(edit_window)
    entry_email.grid(row=3, column=1)
    entry_email.insert(0, current.email)

    (
        tk.Button(
            edit_window, text="Zapisz", command=save_edited_contact
        ).grid(row=4, column=0, columnspan=2)
    )
