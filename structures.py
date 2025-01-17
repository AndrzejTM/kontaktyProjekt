class ContactNode:
    def __init__(self, contact_id, first_name, last_name, phone_number, email):
        self.contact_id = contact_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, contact):
        new_node = ContactNode(*contact)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def sort(self, key):
        if not self.head or not self.head.next:
            return  # No need to sort if the list is empty or has one element

        # Convert the linked list to a list of nodes for easier sorting
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next

        # Sort nodes based on the specified key
        nodes.sort(key=lambda node: getattr(node, key))

        # Rebuild the doubly linked list from the sorted nodes
        self.head = nodes[0]
        self.head.prev = None
        current = self.head
        for i in range(1, len(nodes)):
            current.next = nodes[i]
            nodes[i].prev = current
            current = nodes[i]
        self.tail = current
        self.tail.next = None