class LengthError(Exception):  # Class name follows PascalCase
    def __init__(self, message, error_code):
        super().__init__(message)  # Store message in the built-in args
        self.error_code = error_code

    def __str__(self):
        return f"{self.args[0]} (Error Code: {self.error_code})"  # Access message from args[0]




class get_sum_elements:
    def __init__(self):
        pass

    def get_sum(self,n,li):
        if len(li)!= n:
            raise LengthError("Length error",400)

        flag = True
        for i in li:
            flag = flag and not isinstance(i,(int,float))
        x = 0
        for i in li:
            x+=i
        
        return x

                    


