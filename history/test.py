from z3 import *

arr = [[Int('a_%d_%d' % (i + 1, j + 1)) for i in range(4)] for j in range(4)]
info = [Int('a_%d' % (i + 1)) for i in range(4)]
con1 = [Int('a_%d' % (i + 1)) for i in range(4)]
# con1List = [z3.Int(n) for n in con1]
# con1 = Array('con1', IntSort(), IntSort())
# x = Array('x', IntSort(), IntSort())
# y = Array('y', IntSort(), IntSort())
p = Int('p')
q = Int('q')
r = Int('r')

# len1 = Int('len1')
# len2 = Int('len2')

x = [Int('x_%d' % (i + 1)) for i in range(4)]
y = [Int('y_%d' % (i + 1)) for i in range(4)]

# 初始条件，数字表示提示数，0表示free，1表示re，2表示cl
# con1 = (0, 1, 2, 1)
# con1 = (1, 2, 3, 4)
# con1 = Store(con1, 0, 1)
# con1 = Store(con1, 1, 2)
# con1 = Store(con1, 2, 3)
# con1 = Store(con1, 3, 4)

# 初始条件，数字表示关系，1-8分别表示方位，0表示自身关系，N,E,S,W,NE,SE,SW,NW
con2 = ((0, 2, 2, 5),
        (4, 0, 2, 5),
        (4, 4, 0, 5),
        (7, 7, 7, 0))


# 判断的逻辑公式规则约束：((re E cl) EN re) and re W free
def Inside(a, x):
    # for i in range(LenArr(b)):
    print(type(a))
    for i in range(len(x)):
        print(type(x[i]))
        if a == (x[i]):
            print(1)
            return True
    return False

# 计算arr中非0部分数量
def LenArr(arr):
    arr_len = 0
    i = 0
    while True:
        try:
            val = arr[i]
            if(val != 0):
                arr_len += 1
                i += 1
        except Z3Exception:
            break
    return arr_len

def Pos(a, c):
    for i in range(len(c)):
        if a == c[i]:
            return i
    return 0

def Combine(x, y, c):
    return Exists([r], Implies(And(LenArr(x) > 0, LenArr(y) > 0, Inside(r, c)), Or(Inside(r, x), Inside(r, y))))


# Relation_E函数判断分开后空间是否满足关系
def Relation_E(c, con2):
    return Exists([x, y, p, q], And(Inside(p, x), Inside(q, y), Combine(x, y, c), con2[Pos(p, c)][Pos(q, c)] == 2))


# print([con1[i] for i in range(LenArr(con1))])
# print(con2[0][1])
s = Solver()
s.add([con1[i] == i+1 for i in range(4)])
# s.add(Exists([r], And(r==x[i] ,(r == con1[i] for i in range(len(con1))))))
s.add(Inside(p, con1))
# s.add([Store(con1, 0, 1), Store(con1, 1, 2), Store(con1, 2, 3), Store(con1, 3, 4)])
# s.add(con1.size() == 4)
# s.add(Select(con1, 0) == 3)
check = s.check()
print(s.check())
# model = s.model()
# print(model[x[1]])
# print(model.evaluate(con1[0]))
# s.add(Combine(x, y, con1))
# check = s.check()  # 4、检测是否有解（有解sat、无解unsat）
# print(check)
# model = s.model()  # 5、取出所有结果，一个ModelRef类，
# print(model)
