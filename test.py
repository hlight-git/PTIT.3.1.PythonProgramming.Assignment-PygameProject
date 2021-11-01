class tqh:
    def __init__(self):
        self.var = [1, 2, 3, 4]
    def sds(self):
        self.var += [5, 6]
def fun(tqhh):
    tqhh.var -= 10
var = [1, 2, 3, 4, 5]
def func(var):
    var.pop(1)

t = tqh()
l = [tqh(), t, tqh()]
for ele in l:
    ele.sds()
for ele in l:
    print(ele.var)

if 1 < 2 < 3 < 4:
    print(111)