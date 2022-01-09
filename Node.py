
class Node(object):

    def __init__(self, item = None, parent = None):
        self.item = item
        self.parent = parent

    def __str__(self):
        return f'NODE({self.item}, {self.parent})'

    def __repr__(self):
        return f'NODE({self.item}, {self.parent})'






