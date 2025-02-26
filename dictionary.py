class Square:
    def __init__(self, numbers):
        self.numbers = numbers
    
    def square_number(self, num):
        return num ** 2
    
    def get_squared_dict(self):
        return dict(map(lambda num: (num, self.square_number(num)), self.numbers))

# Example usage
numbers = [1, 2, 3, 4, 5]
square_obj = Square(numbers)
squared_numbers_dict = square_obj.get_squared_dict()
print("Original numbers:", numbers)
print("Squared numbers dictionary:", squared_numbers_dict)
