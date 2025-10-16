class Node:
    def __init__(self, val: int):
        self.val = val
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def push_front(self, x: int):
        node = Node(x)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1

    def push_back(self, x: int):
        node = Node(x)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def pop_front(self):
        if self.is_empty():
            print("List is empty.")
            return
        val = self.head.val
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self._size -= 1
        print("Deleted from front:", val)

    def pop_back(self):
        if self.is_empty():
            print("List is empty.")
            return
        val = self.tail.val
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self._size -= 1
        print("Deleted from back:", val)

    def update_first(self, old_val: int, new_val: int):
        cur = self.head
        while cur:
            if cur.val == old_val:
                cur.val = new_val
                print(f"Updated first occurrence of {old_val} to {new_val}.")
                return
            cur = cur.next
        print(f"Value {old_val} not found.")

    def to_list(self):
        out = []
        cur = self.head
        while cur:
            out.append(cur.val)
            cur = cur.next
        return out

    def show(self):
        print("List:", self.to_list(), f"(size={self._size})")


def get_int(prompt: str):
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("Please enter an integer.")

def menu():
    ll = DoublyLinkedList()
    actions = {
        "1": lambda: ll.push_front(get_int("Enter integer to insert at FRONT: ")),
        "2": lambda: ll.push_back(get_int("Enter integer to insert at BACK: ")),
        "3": ll.pop_front,
        "4": ll.pop_back,
        "5": lambda: ll.update_first(
                get_int("Enter OLD integer value to update: "),
                get_int("Enter NEW integer value: ")
             ),
        "6": ll.show,
        "0": lambda: (_ for _ in ()).throw(SystemExit),
    }

    while True:
        print("\n--- Linked List Menu ---")
        print("1) Insert front")
        print("2) Insert back")
        print("3) Delete front")
        print("4) Delete back")
        print("5) Update first occurrence")
        print("6) Read (print) list")
        print("0) Exit")
        choice = input("Choose: ").strip()
        action = actions.get(choice)
        try:
            if action:
                action()
            else:
                print("Invalid choice.")
        except SystemExit:
            print("Goodbye!")
            break
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    menu()
