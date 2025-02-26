class ListManager:
    def __init__(self, elements):
        self.elements = elements
    
    def display_list(self):
        print("\nList containing multiple values: ")
        print(self.elements)
    
    def access_element(self, index):
        return self.elements[index]
    
    def access_negative_index(self, index):
        return self.elements[index]

# Example usage
list1 = ListManager(["Geeks", "For", "Geeks"])
list1.display_list()
print("Accessing element from the list")
print(list1.access_element(0))  
print(list1.access_element(2))

# Multi-Dimensional List class
class MultiDimensionalList:
    def __init__(self, elements):
        self.elements = elements
    
    def display_list(self):
        print("\nMulti-Dimensional List: ")
        print(self.elements)

multi_list = MultiDimensionalList([["Geeks", "For"], ["Geeks"]])
multi_list.display_list()

print("Accessing element using negative indexing")
print(list1.access_negative_index(-1))
print(list1.access_negative_index(-3))
