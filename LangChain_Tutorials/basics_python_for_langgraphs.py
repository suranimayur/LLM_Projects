
<<<<<<< HEAD
'''
Typed Dictionary


'''

from typing import TypedDict

class Movie(TypedDict):
    name: str
    year: int

movie = Movie(name="Avenge Endgame",year=2019)

print(movie)

'''
Union

'''

from typing import Union

def add(a: Union[int, float], b: Union[int, float]) -> Union[float]:
    return a + b

print(add(1, 2))
print(add(1.5, 2.5))
print(add("1", "2"))  # This will raise a TypeError

'''
Optional
'''
from typing import Optional

def nice_message(name: Optional[str]) -> None:
    if name is None:
        print("hey random person")
    else:
        print(f"Hi, There, {name}!! ")

from typing import Any

def print_person(person: dict[str, Any]) -> None:
    print(f"Name: {person['name']}")
    print(f"Age: {person['age']}")
    print(f"City: {person['city']}")
    print(f"Phone: {person['phone']}")
    print(f"Address: {person['address']}")
    print(f"Last Name: {person['lastname']}")


'''

Lambda Function

'''

square = lambda x: x*x 
square(29)

num = [1,2,3,4]

squares = list(map(lambda x: x * x,num))

print(squares)

## Elements in Langgraph
'''

'''



=======
>>>>>>> 6f9c51b (daily post)























