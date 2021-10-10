class tqh:
    def __init__(self):
        self.var = 23

def fun(tqhh):
    tqhh.var -= 10
var = [1, 2, 3, 4, 5]
def func(var):
    var.pop(1)

tqhh = tqh()
fun(tqhh)
func(var)
print(tqhh.var)
print(var)