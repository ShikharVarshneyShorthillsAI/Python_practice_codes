# Tuple Manager class
class TupleManager:
    def __init__(self, elements):
        self.elements = tuple(elements)
    
    def display_tuple(self):
        print("\nTuple: ")
        print(self.elements)
    
    def access_element(self, index):
        return self.elements[index]

# Example usage
tuple1 = TupleManager(("Geeks", "For"))
tuple1.display_tuple()

list1 = [1, 2, 4, 5, 6]
tuple2 = TupleManager(list1)
print("\nTuple using List: ")
tuple2.display_tuple()

print("First element of tuple:", tuple2.access_element(0))
print("Last element of tuple:", tuple2.access_element(-1))
print("Third last element of tuple:", tuple2.access_element(-3))
