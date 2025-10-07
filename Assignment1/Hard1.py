#Optimize the implementation of Python Basics & Setup for performance In Easy2

from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class Stack(Generic[T]):
    __slots__ = ("_a",)
    def __init__(self, iterable: Optional[List[T]] = None):
        self._a: List[T] = list(iterable or ())
    def push(self, x: T) -> None:
        self._a.append(x)         
    def pop(self) -> T:
        if not self._a:
            raise IndexError("pop from empty stack")
        return self._a.pop()     
    def peek(self) -> T:
        if not self._a:
            raise IndexError("peek on empty stack")
        return self._a[-1]        
    def clear(self) -> None:
        self._a.clear()
    def to_list(self) -> List[T]:
        return self._a.copy()
    def __len__(self) -> int:
        return len(self._a)
    def __bool__(self) -> bool:
        return bool(self._a)

def menu():
    s = Stack[int]()
    actions = {
        "1": lambda: s.push(int(input("Element: "))),
        "2": lambda: print("Popped:", s.pop()),
        "3": lambda: print("Top:", s.peek()),
        "4": lambda: print("Stack:", s.to_list()),
        "5": lambda: (s.clear(), print("Cleared")),
        "0": lambda: (_ for _ in ()).throw(SystemExit),
    }
    while True:
        print("\n1.Push  2.Pop  3.Top  4.Show  5.Clear  0.Exit")
        choice = input("Choose: ").strip()
        try:
            action = actions.get(choice)
            if action: action()
            else: print("Invalid choice")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    menu()
