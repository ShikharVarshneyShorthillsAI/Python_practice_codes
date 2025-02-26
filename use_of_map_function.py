class Square:
    def __init__(self, numbers):
        self.numbers = numbers
    
    def square_number(self, num):
        return num ** 2
    
    def get_squared_list(self):
        return list(map(self.square_number, self.numbers))

# Example usage
numbers = [1, 2, 3, 4, 5]
square_obj = Square(numbers)
squared_numbers = square_obj.get_squared_list()
print("Original numbers:", numbers)
print("Squared numbers:", squared_numbers)
