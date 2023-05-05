from z3 import *

# 定义一个存储的Arr，第1行用于存储标记(1,2,3,4)
# 第2-4行用于存储标记内含有的信息(第2行表示re，第3行表示cl，第四行表示free)
# 第5行——最后一行与列长一致，形成空间关系表
arr = [[Int("x_%s_%s" % (i+1, j+1)) for j in range(4)]
       for i in range(8)]

# 定义两行带求解的返回数组result
result = [[Int('r_%d_%d' % (i + 1, j + 1)) for j in range(4)]
          for i in range(2)]

# 添加限制，将arr的信息录入，数字表示关系，1-8分别表示方位，0表示自身关系，N,E,S,W,NE,SE,SW,NW
con2 = ((1, 2, 3, 4),
        (0, 1, 0, 1),
        (0, 0, 1, 0),
        (1, 0, 0, 0),
        (0, 2, 2, 5),
        (4, 0, 2, 5),
        (4, 4, 0, 5),
        (7, 7, 7, 0))

# 第1-8行
info_c = [arr[i][j] == con2[i][j] for i in range(8) for j in range(4)]

# 添加result的限制，每一列信息不能相等
cols_c = [z3.Distinct([result[i][j] for i in range(2)])
          for j in range(4)]

# 添加result的限制，只能为1或者0
result_c = [And(result[i][j] >= 0, result[i][j] <= 1) for i in range(2) for j in range(4)]

# 添加要判断的公式的约束，例如(re E cl) and re W free
# 找到re
formula_c1 = [Or([And(result[0][j] == 1, arr[1][j] == 1) for j in range(4)])]
# 找到cl
formula_c2 = [Or([And(result[1][j] == 1, arr[2][j] == 1) for j in range(4)])]
# 找到free
formula_c3 = [Or([And(result[1][j] == 1, arr[3][j] == 1) for j in range(4)])]
# 存在方位关系EN方是re free，re and cl
formula_c4 = [Or([And(result[0][i] == 1, result[1][j] == 1, arr[1][i] == 1, arr[1][j] == 1, arr[i+4][j] == 5) for j in range(4) for i in range(4)])]
# 存在方位关系W
formula_c5 = [Or([And(result[0][i] == 1, result[1][j] == 1, arr[i+4][j] == 4) for j in range(4) for i in range(4)])]

# (re E cl) and re W free
formula_tol1 = formula_c1 + formula_c2 + formula_c3 + formula_c4 + formula_c5
# re WS re
formula_tol2 = [Or([And(result[0][i] == 1, result[1][j] == 1, arr[1][i] == 1, arr[1][j] == 1, arr[i+4][j] == 7) for j in range(4) for i in range(4)])]

# 求解器
s = Solver()
s.add(info_c + cols_c + formula_tol2 + result_c)
check = s.check()
print(s.check())
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(result[i][j]) for j in range(4)]
         for i in range(2)]
    print_matrix(r)
else:
    print("failed to solve")
