#Solve a toy example applying Python Basics & Setup

class Stack:
    def __init__(self):
         self.arr=[]
         self.top=-1
    def push(self,x):
         self.arr.append(x)
         self.top+=1
    def pop(self):
         x=self.arr.pop()
         print("Popped element: ",x)
         self.top-=1
    def tops(self):
         print("Top element: ",self.arr[self.top])
    def show(self):
         print(self.arr)
# Menu Driven Programming 
array=Stack()
while(True):
    print("1. Instert the element\n2.Pop an element\n3.top element\n4. show the array ")
    x=int(input("Enter the number to perform the operations on the Stack: "))
    if (x==1):
         element=int(input("Enter the element:"))
         array.push(element)
    elif(x==2):
         array.pop()
    elif(x==3):
         array.tops()
    elif(x==4):
         array.show()
    
          
          

