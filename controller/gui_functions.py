import tkinter as tk
from tkinter import messagebox
from model.db.database import add_contact_to_db, delete_contact_from_db
from model.structures import ChangesStack, ContactNode

undo_stack = ChangesStack()
redo_stack = ChangesStack()


def sort_contacts_by_column(tree, column, contacts):
    # Sort contacts by the chosen column (first_name or last_name)
    contacts.sort(column)
    refresh_contacts(tree, contacts)


def refresh_contacts(tree, contact_list):
    tree.delete(*tree.get_children())
    current = contact_list.head
    while current:
        tree.insert(
            "",
            "end",
            iid=current.contact_id,
            values=(
                current.contact_id,
                current.first_name,
                current.last_name,
                current.phone_number,
                current.email,
            ),
        )
        current = current.next


def add_contact(
    add_window, contact_list, tree, first_name, last_name, phone_number, email
):
    if not first_name or not last_name or not phone_number:
        messagebox.showerror(
            "Błąd", "Wszystkie pola oprócz email są wymagane."
        )
        return

    contact_id = add_contact_to_db(first_name, last_name, phone_number, email)
    contact_list.append(
        (contact_id, first_name, last_name, phone_number, email)
    )
    undo_stack.push(
        "delete",
        ContactNode(contact_id, first_name, last_name, phone_number, email),
    )
    refresh_contacts(tree, contact_list)
    messagebox.showinfo("Sukces", "Kontakt dodany.")
    add_window.destroy()


def delete_contact(contact_list, tree, contact_id):
    current = contact_list.head
    while current:
        if current.contact_id == contact_id:
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            if current == contact_list.head:
                contact_list.head = current.next
            if current == contact_list.tail:
                contact_list.tail = current.prev
            delete_contact_from_db(contact_id)
            undo_stack.push("add", current)
            refresh_contacts(tree, contact_list)
            messagebox.showinfo("Sukces", "Kontakt został usunięty.")
            return
        current = current.next


def undo_last_action(contact_list, tree):
    if undo_stack.is_empty():
        messagebox.showwarning("Uwaga", "Nie ma nic do cofnięcia.")
        return

    action, data = undo_stack.pop()
    if action == "delete":
        delete_contact_from_db(data.contact_id)
        delete_contact(contact_list, tree, data.contact_id)
        redo_stack.push("add", data)
    elif action == "add":
        data.contact_id = add_contact_to_db(
            data.first_name, data.last_name, data.phone_number, data.email
        )
        redo_stack.push("delete", data)
        contact_list.append(
            (
                data.contact_id,
                data.first_name,
                data.last_name,
                data.phone_number,
                data.email,
            )
        )
        messagebox.showinfo("Sukces", "Kontakt dodany.")
    refresh_contacts(tree, contact_list)
    messagebox.showinfo("Sukces", "Ostatnia akcja została cofnięta.")


def redo_last_action(contact_list, tree):
    if redo_stack.is_empty():
        messagebox.showwarning("Uwaga", "Nie ma nic do przywrócenia.")
        return

    action, data = redo_stack.pop()
    if action == "delete":
        delete_contact_from_db(data.contact_id)
        delete_contact(contact_list, tree, data.contact_id)
    elif action == "add":
        data.contact_id = add_contact_to_db(
            data.first_name, data.last_name, data.phone_number, data.email
        )
        contact_list.append(
            (
                data.contact_id,
                data.first_name,
                data.last_name,
                data.phone_number,
                data.email,
            )
        )
        undo_stack.push("delete", data)
        messagebox.showinfo("Sukces", "Kontakt przywrócony.")
    refresh_contacts(tree, contact_list)
    messagebox.showinfo("Sukces", "Ostatnia akcja została przywrócona.")


def search_contacts(tree, entry_search, contact_list):
    query = entry_search.get().lower()
    if not query:
        messagebox.showwarning("Uwaga", "Pole wyszukiwania jest puste.")
        return

    tree.delete(*tree.get_children())

    contacts = []
    current = contact_list.head
    while current:
        contact_data = (
            f"{current.first_name} "
            f"{current.last_name} "
            f"{current.phone_number} "
            f"{current.email or ''}".lower()
        )
        if query in contact_data:  # Filtruj kontakty na podstawie zapytania
            contacts.append(current)
        current = current.next

    if not contacts:
        messagebox.showinfo(
            "Informacja",
            "Nie znaleziono kontaktów pasujących do zapytania.",
        )
        return

    for contact in contacts:
        tree.insert(
            "",
            "end",
            iid=contact.contact_id,
            values=(
                contact.contact_id,
                contact.first_name,
                contact.last_name,
                contact.phone_number,
                contact.email,
            ),
        )


def filter_contacts_by_letter(letter, tree, contact_list):
    tree.delete(*tree.get_children())
    current = contact_list.head
    while current:
        if current.last_name.lower().startswith(letter.lower()):
            tree.insert(
                "",
                "end",
                iid=current.contact_id,
                values=(
                    current.contact_id,
                    current.first_name,
                    current.last_name,
                    current.phone_number,
                    current.email,
                ),
            )
        current = current.next

    # Logic for deleting selected contact


def delete_selected_contact(tree, contact_list):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Błąd", "Nie wybrano kontaktu do usunięcia.")
        return

    contact_id = int(selected_item)
    delete_contact(contact_list, tree, contact_id)


def reset_search(tree, entry_search, contact_list):
    entry_search.delete(0, tk.END)  # Clear search field
    refresh_contacts(tree, contact_list)  # Reset whole list
