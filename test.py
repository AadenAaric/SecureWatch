# def game():
#     Ans = ""
#     while True:
        
#         if Ans == "yes":
#             continue
#         else:
#             break
#         print("Guess The Personality!")
#         Guess = input("Enter your Guess: ")
#         Ans = input("Guess The name: ")

#         x = 3
#         while x > 1:
#             x = x-1
#             if Guess != Ans:
#                 Ans = input("Guess The name: ")
#             else:
#                 print("You won!")
#                 Ans = str(input("Do you want to continue?"))
                
#         else:
#             print("YOU DIED!")
#             Ans = input("Do you want to continue?")
#             if Ans == "no":
#                 break
#             else:
#                 continue

# game()


class Parent():

    _emp_name = None
    _emp_age = None
    ls = [1,2,3,4,5]
    i = 0
    

    def __init__(self, __emp_name , __emp_age):
        self._emp_name = __emp_name
        self._emp_age = __emp_age

    def __next__(self):
      if self.i < len(self.ls):
        self.i += 1
        return self.ls[self.i-1]
      else:
         raise StopIteration

class Child(Parent):
    
    def __init__(self, __emp_name, __emp_age, salary):
       super().__init__(__emp_name, __emp_age)
       self.salary = salary
       
    def getName(self):
       return self._emp_name


obj = Child("talha",22,15000)

from threading import Thread

def func1(i):
   print(f"func{i} started!")
   import time
   time.sleep(i)
   print(f"func{i} Completed!")

# Th1 = Thread(target=func1, args=(1,))
# Th2 = Thread(target=func1, args=(2,))
# Th1.start()
# Th2.start()

def lowercase(func):
   def wrapper(*args,**kwargs):
      result = func(*args,**kwargs)
      if isinstance(result, str):
            result = result.lower()
      return result
   return wrapper




@lowercase
def sayhello(i):
   return i


print(sayhello("HELLO"))
