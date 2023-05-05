from z3 import *
r = [[Int("r_%s_%s" % (i + 1, j + 1)) for j in range(4)] for i in range(5)]
re = [[Int("re_%s_%s" % (i + 1, j + 1)) for j in range(2)] for i in range(5)]
cl = [[Int("cl_%s_%s" % (i + 1, j + 1)) for j in range(2)] for i in range(5)]
fr = [[Int("f_%s_%s" % (i + 1, j + 1)) for j in range(4)] for i in range(2)]
pth = [[Int("p_%s_%s" % (i + 1, j + 1)) for j in range(4)] for i in range(2)]
result = [[Int('x_%d_%d' % (i + 1, j + 1)) for j in range(5)] for i in range(8)]
rx = ((1, 2, 3, 4),
      (0, 1, 1, 8),
      (5, 0, 1, 8),
      (5, 5, 0, 8),
      (4, 4, 4, 0))

rex = ((101, 102),
       (0,    0),
       (1,    0),
       (0,    0),
       (0,    1))

clx = ((101, 102),
       (0,    0),
       (0,    0),
       (0,    1),
       (0,    0))

frx = ((1, 2, 3, 4),
       (1, 0, 0, 0))

pthx = ((2, 1, 0, 0),
        (4, 3, 2, 1))
info_c1 = [r[i][j] == rx[i][j] for i in range(5) for j in range(4)]
# info_c1 = [r[i][j] == rx[i][j] for i in range(5) for j in range(4)]

info_c2 = [re[i][j] == rex[i][j] for i in range(5) for j in range(2)]
# info_c2 = [re[i][j] == rex[i][j] for i in range(5) for j in range(2)]

info_c3 = [cl[i][j] == clx[i][j] for i in range(5) for j in range(2)]
# info_c3 = [cl[i][j] == clx[i][j] for i in range(5) for j in range(2)]

info_c4 = [fr[i][j] == frx[i][j] for i in range(2) for j in range(4)]
# info_c4 = [fr[i][j] == frx[i][j] for i in range(2) for j in range(4)]

info_c5 = [pth[i][j] == pthx[i][j] for i in range(2) for j in range(4)]
# info_c5 = [pth[i][j] == pthx[i][j] for i in range(2) for j in range(4)]

info_c = info_c1 + info_c2 + info_c3 + info_c4 + info_c5
# info_c = info_c1 + info_c2 + info_c3 + info_c4 + info_c5

formula_rz1 = [And([Implies(And(result[z][j+1] == 1, i != j), result[z][i+1] == 0) for i in range(4) for j in range(4)]) for z in [4, 5, 6, 7]]
# formula_rz1 = [And([Implies(And(result[z][j+1] == 1, i != j), result[z][i+1] == 0) for i in range(4) for j in range(4)]) for z in [4, 5, 6, 7]]

formula_rz2 = [And(Implies(Or([And(result[4][i+1] == 1, re[i+1][0] == 1) for i in range(4)]), result[4][0] == 1), Implies(And([Implies(result[4][i+1] == 1, re[i+1][0] == 0) for i in range(4)]), result[4][0] == 0))]
# formula_rz2 = [And(Implies(Or([And(result[4][i+1] == 1, re[i+1][0] == 1) for i in range(4)]), result[4][0] == 1), Implies(And([Implies(result[4][i+1] == 1, re[i+1][0] == 0) for i in range(4)]), result[4][0] == 0))]

formula_rz3 = [And(Implies(Or([And(result[5][i+1] == 1, cl[i+1][1] == 1) for i in range(4)]), result[5][0] == 1), Implies(And([Implies(result[5][i+1] == 1, cl[i+1][1] == 0) for i in range(4)]), result[5][0] == 0))]
# formula_rz3 = [And(Implies(Or([And(result[5][i+1] == 1, cl[i+1][1] == 1) for i in range(4)]), result[5][0] == 1), Implies(And([Implies(result[5][i+1] == 1, cl[i+1][1] == 0) for i in range(4)]), result[5][0] == 0))]

formula_rz4 = [And(And(Or([And(result[6][i+1] == 1, re[i+1][0] == 1) for i in range(4)]), result[6][0] == 1), And((And([Implies(result[6][i+1] == 1, re[i+1][0] == 0) for i in range(4)])), result[6][0] == 0))]
# formula_rz4 = [And(Implies(Or([And(result[6][i+1] == 1, re[i+1][0] == 1) for i in range(4)]), result[6][0] == 1), Implies(And([Implies(result[6][i+1] == 1, re[i+1][0] == 0) for i in range(4)]), result[6][0] == 0))]

formula_rz5 = [And(Implies(Or([And(result[7][i+1] == 1, re[i+1][1] == 1) for i in range(4)]), result[7][0] == 1), Implies(And([Implies(result[7][i+1] == 1, re[i+1][1] == 0) for i in range(4)]), result[7][0] == 0))]
# formula_rz5 = [And(Implies(Or([And(result[7][i+1] == 1, re[i+1][1] == 1) for i in range(4)]), result[7][0] == 1), Implies(And([Implies(result[7][i+1] == 1, re[i+1][1] == 0) for i in range(4)]), result[7][0] == 0))]

formula_con = formula_rz1 + formula_rz2 + formula_rz3 + formula_rz4 + formula_rz5
# formula_con = formula_rz1 + formula_rz2 + formula_rz3 + formula_rz4 + formula_rz5

formula_pre = [And(result[0][1] == 0, result[0][2] == 1, result[0][3] == 1, result[0][4] == 1)]
# formula_pre = [And(result[0][1] == 0, result[0][2] == 1, result[0][3] == 1, result[0][4] == 1)]

formula_const1 = [And([And(Implies(result[0][j+1] == 1, Or(result[1][j+1] == 1, result[1][j+1] == 0)), Implies(result[0][j+1] == 0, result[1][j+1] == 0)) for j in range(4)])]
# formula_const0x = [And([And(Implies(result[0][j+1] == 1, Or(result[1][j+1] == 1, result[1][j+1] == 0)), Implies(result[0][j+1] == 0, result[1][j+1] == 0)) for j in range(4)])]

formula_res1 = [And(Implies(result[1][0] == 0, result[0][0] == 1), Implies(result[1][0] == 1, result[0][0] == 0))]
# formula_prex = [And(Implies(result[1][0] == 0, result[0][0] == 1), Implies(result[1][0] == 1, result[0][0] == 0))]

formula_const2 = [And([And(Implies(result[1][j+1] == 1, And(Or(result[2][j+1] == 1, result[2][j+1] == 0), Or(result[3][j+1] == 1, result[3][j+1] == 0))), Implies(result[1][j+1] == 0, And(result[2][j+1] == 0, result[3][j+1] == 0))) for j in range(4)])]
# formula_const1 = [And([And(Implies(result[1][j+1] == 1, And(Or(result[2][j+1] == 1, result[2][j+1] == 0), Or(result[3][j+1] == 1, result[3][j+1] == 0))), Implies(result[1][j+1] == 0, And(result[2][j+1] == 0, result[3][j+1] == 0))) for j in range(4)])]

# formula_res2 = [And(Implies(And(result[2][0] == 1, result[3][0] == 1), result[1][0] == 1), Implies(Or(result[2][0] == 0, result[3][0] == 0), result[1][0] == 0))]
# formula_res3 = [And(Implies(And(result[4][0] == 1, result[5][0] == 1), result[2][0] == 1), Implies(Or(result[4][0] == 0, result[5][0] == 0), result[2][0] == 0))]
# formula_res4 = [And(Implies(And(result[6][0] == 1, result[7][0] == 1), result[3][0] == 1), Implies(Or(result[6][0] == 0, result[7][0] == 0), result[3][0] == 0))]
formula_const1x = [And(Implies(And(result[2*i][0] == 1, result[2*i+1][0] == 1), result[i][0] == 1), Implies(Or(result[2*i][0] == 0, result[2*i+1][0] == 0), result[i][0] == 0)) for i in [1, 2, 3]]

formula_s_x1 = [Or([And(result[4][i+1] == 1, result[5][j+1] == 1, r[i+1][j] == 1) for j in range(4) for i in range(4)])]
# formula_s_x1 = [Or([And(result[4][i+1] == 1, result[5][j+1] == 1, r[i+1][j] == 1) for j in range(4) for i in range(4)])]

formula_const3 = [And([And(Implies(result[2][j+1] == 1, Or(And(result[4][j+1] == 1, result[5][j+1] == 0), And(result[4][j+1] == 0, result[5][j+1] == 1))), Implies(result[2][j+1] == 0, And(result[4][j+1] == 0, result[5][j+1] == 0))) for j in range(4)])]
# formula_const2 = [And([And(Implies(result[2][j+1] == 1, Or(And(result[4][j+1] == 1, result[5][j+1] == 0), And(result[4][j+1] == 0, result[5][j+1] == 1))), Implies(result[2][j+1] == 0, And(result[4][j+1] == 0, result[5][j+1] == 0))) for j in range(4)])]


formula_s_x2 = [Or([And(result[6][i+1] == 1, result[7][j+1] == 1, r[i+1][j] == 8) for j in range(4) for i in range(4)])]
# formula_s_x2 = [Or([And(result[6][i+1] == 1, result[7][j+1] == 1, r[i+1][j] == 8) for j in range(4) for i in range(4)])]

formula_const4 = [And([And(Implies(result[3][j+1] == 1, Or(And(result[6][j+1] == 1, result[7][j+1] == 0), And(result[6][j+1] == 0, result[7][j+1] == 1))), Implies(result[3][j+1] == 0, And(result[6][j+1] == 0, result[7][j+1] == 0))) for j in range(4)])]
# formula_const3 = [And([And(Implies(result[3][j+1] == 1, Or(And(result[6][j+1] == 1, result[7][j+1] == 0), And(result[6][j+1] == 0, result[7][j+1] == 1))), Implies(result[3][j+1] == 0, And(result[6][j+1] == 0, result[7][j+1] == 0))) for j in range(4)])]

formula_s = formula_s_x1 + formula_s_x2

con_3 = formula_res1 + formula_const1x
con_const = formula_pre + formula_const1 + formula_const2 + formula_const3 + formula_const4 + con_3 + formula_s

s = Solver()
s.add(info_c + con_const + formula_con)
check = s.check()
print(s.check())
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(result[i][j]) for j in range(5)] for i in range(8)]
    print_matrix(r)
else:
    print("failed to solve")
