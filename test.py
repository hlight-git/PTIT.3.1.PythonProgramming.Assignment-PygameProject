from pygame import Vector2

class F:
    def __init__(self, tqh):
        self.tqh = tqh
    
    def update(self):
        print(1)

class H(F):
    def __init__(self, tqh):
        super().__init__(tqh)
    
h = H('tqh')
h.update()
print(not True)