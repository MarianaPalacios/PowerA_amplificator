class stack():
    def __init__(self):
        self.item = []

    def push(self,item):
        self.item.append(item)

    def is_empty(self):
        return self.item == []

    def __str__(self):
        return f'Asi va el vector {self.item}'

    def get_stack(self):
        return self.item

    def Empty(self):
        self.item = []

    def listToString(self):
        self.str = ""
        for self.i in self.item:
            self.str += self.i
        return self.str

