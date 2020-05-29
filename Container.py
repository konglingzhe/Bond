# 以下是容器
class Attr:
    '''Attribute
    '''
    def __init__(self):
        self.value = None
    
    def add_value(self, value):
        self.value = value 

class Bond:
    bond_name_list = []
    def __init__(self):
        self._attrs = {}
    def attr(self, name):
        if name not in self._attrs:
            self._attrs[name] = Attr()
        return self._attrs[name]    


class Bondbook:
    def __init__(self):
        self._bonds = {}
    def bond(self, name):
        if name not in self._bonds:
            self._bonds[name] = Bond()
            Bond.bond_name_list.append(name)
        return self._bonds[name]