from tkinter import messagebox
from database import add_contact_to_db, delete_contact_from_db
from structures import UndoStack, ContactNode

undo_stack = UndoStack()

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
        messagebox.showerror("Błąd", "Wszystkie pola oprócz email są wymagane.")
        return

    contact_id = add_contact_to_db(first_name, last_name, phone_number, email)
    contact_list.append((contact_id, first_name, last_name, phone_number, email))
    undo_stack.push("delete", ContactNode(contact_id, first_name, last_name, phone_number, email))
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
    elif action == "add":
        data.contact_id = add_contact_to_db(data.first_name, data.last_name, data.phone_number, data.email)
        contact_list.append((data.contact_id, data.first_name, data.last_name, data.phone_number, data.email))
        messagebox.showinfo("Sukces", "Kontakt dodany.")
    refresh_contacts(tree, contact_list)
    messagebox.showinfo("Sukces", "Ostatnia akcja została cofnięta.")