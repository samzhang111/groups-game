class Group(object):
    def __init__(self, name, S, table):
        self.name = name
        self.S = S
        self.table = table
        self.validate_shape()
        self.ident = self.find_identity()

    def validate_shape(self):
        N = len(set(self.table.keys()))
        for elem in self.table:
            if len(self.table[elem]) != len(self.S):
                raise ValueError("Multiplication table has mismatched sizes for entry {}. Expected {}, received {}.".format(elem, len(self.S), len(self.table[elem])))

            if len(set(self.table[elem])) != N:
                raise ValueError("Multiplication table lacks Latin Square property.")

    def find_identity(self):
        for elem in self.table:
            i = 0
            for val in self.S:
                if self.table[elem][val] == val and self.table[val][elem] == val:
                    i += 1

            if i == len(self.S):
                ident = elem

        if not ident:
            raise ValueError("No two-sided identity found in table.")

        return ident

    def multiply(self, left, right):
        return self[self.table[left][right]]

    def __getitem__(self, key):
        if key not in self.S:
            raise ValueError("Element {} not in group {}".format(key, self.name))

        return GroupElement(self, key)

class GroupElement(object):
    def __init__(self, group, elem):
        if elem not in group.S:
            raise ValueError("Element {} not in group {}".format(elem, group.name))

        self.group = group
        self.elem = elem

    def __mul__(self, other):
        if not type(other) == GroupElement:
            raise ValueError("GroupElements can only multiply with other GroupElements")
        if other.group != self.group:
            raise ValueError("Cannot multiply elements of different groups: {} and {}".format(self.group.name, other.group.name))

        return self.group.multiply(self.elem, other.elem)

    def __repr__(self):
        return "<{}: {}>".format(self.group.name, self.elem)
