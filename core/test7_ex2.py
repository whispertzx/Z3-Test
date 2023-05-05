from z3 import *

# /**
#   (1)转化前步骤
#   (2)信息约束
#   (3)初始行约束和原子公式行约束[将公式中每个节点根据节点下放约束(3)将条件加入result集合中]
#   (4)节点下放约束[将公式中第一行初始化条件和原子公式所在的叶子节点行所在约束(4)加入result集合中]
#   (5)求解器构建和结果输出
# */

# /**
#   --------------
#   实例测试
#   example2
#   --------------
# */

r = [[Int("r_%s_%s" % (i+1, j+1)) for j in range(4)]
     for i in range(5)]

re = [[Int("re_%s_%s" % (i+1, j+1)) for j in range(2)]
      for i in range(5)]

cl = [[Int("cl_%s_%s" % (i+1, j+1)) for j in range(2)]
      for i in range(5)]

fr = [[Int("f_%s_%s" % (i+1, j+1)) for j in range(4)]
      for i in range(2)]

pth = [[Int("p_%s_%s" % (i+1, j+1)) for j in range(4)]
       for i in range(3)]

# 对于结果集我们构造一个表，让求解空间划分问题变成寻找这一张表能不能完成类似数独问题的一个解
# 构建一个行数等同于语法树节点数量的结果集，其中列长度等同于区域长度 + 1，其中第一列表示当前值是否为真或假，其中1表示当前行约束存在，0表示不需要进行约束
result = [[Int('x_%d_%d' % (i + 1, j + 1)) for j in range(5)]
          for i in range(8)]

# /**
#   (2)信息约束
# */
# 第一步：录入区域的信息，维护空间关系表，共1张
# 第1行表示区域编号，分别用1-20表示，｜第2行-最后1行｜ == ｜第1列-最后1列｜，存入空间关系表，1-8 ::= E,ES,S,WS,W,WN,N,EN
# example:
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

# 信息录入约束
info_c1 = [r[i][j] == rx[i][j] for i in range(5) for j in range(4)]
info_c2 = [re[i][j] == rex[i][j] for i in range(5) for j in range(2)]
info_c3 = [cl[i][j] == clx[i][j] for i in range(5) for j in range(2)]
info_c4 = [fr[i][j] == frx[i][j] for i in range(2) for j in range(4)]
info_c5 = [pth[i][j] == pthx[i][j] for i in range(2) for j in range(4)]

info_c = info_c1 + info_c2 + info_c3 + info_c4 + info_c5

# /**
#   (3)初始行约束和原子公式行约束
# */

# example2: 例如公式(re(101) B cl(102)) And (re(101) LB re(102))，result集仍为3个，~((re(101) E cl(102) And (re(101) EN re(102)))
#
#                        ~
#                        |
#                       and
#                /              \
#              E                  EN
#           /     \            /      \
#       re(101)  cl(102)   re(101)  re(102)

# 针对叶子节点的约束，依次对应即可
# 基本约束，原子公式区域为1
formula_rz1 = [And([Implies(And(result[z][j+1] == 1, i != j), result[z][i+1] == 0)
                    for i in range(4) for j in range(4)])
               for z in [4, 5, 6, 7]]
# 对于节点5的约束，节点5为re(101)
formula_rz2 = [And(Implies(Or([And(result[4][i+1] == 1, re[i+1][101-101] == 1) for i in range(4)]), result[4][0] == 1),
                  Implies(And([Implies(result[4][i+1] == 1, re[i+1][101-101] == 0) for i in range(4)]), result[4][0] == 0))]
# 对于节点5的约束，节点5为cl(102)：修改为cl(101)
formula_rz3 = [And(Implies(Or([And(result[5][i+1] == 1, cl[i+1][102-101] == 1) for i in range(4)]), result[5][0] == 1),
                  Implies(And([Implies(result[5][i+1] == 1, cl[i+1][102-101] == 0) for i in range(4)]), result[5][0] == 0))]
# 对于节点6的约束，节点6为re(101)
formula_rz4 = [And(Implies(Or([And(result[6][i+1] == 1, re[i+1][101-101] == 1) for i in range(4)]), result[6][0] == 1),
                  Implies(And([Implies(result[6][i+1] == 1, re[i+1][101-101] == 0) for i in range(4)]), result[6][0] == 0))]
# 对于节点7的约束，节点7为re(102)
formula_rz5 = [And(Implies(Or([And(result[7][i+1] == 1, re[i+1][102-101] == 1) for i in range(4)]), result[7][0] == 1),
                  Implies(And([Implies(result[7][i+1] == 1, re[i+1][102-101] == 0) for i in range(4)]), result[7][0] == 0))]

formula_con = formula_rz1 + formula_rz2 + formula_rz3 + formula_rz4 + formula_rz5

# /**
#   (4)节点下放约束
# */

# 针对example3我们给出具体的约束下放实例(re(101) E cl(102)) and (re(101) EN re(102))，给定区域如果为1，2，3，4(结果应该返回sat)
# 初始约束，判断的区域范围
formula_pre = [And(result[0][1] == 0, result[0][2] == 1, result[0][3] == 1, result[0][4] == 1)]

# 初始约束对第2个节点约束
formula_prex = [And(Implies(result[1][0] == 0, result[0][0] == 1), Implies(result[1][0] == 1, result[0][0] == 0))]

# 第1个节点下放到第2个节点的空间
formula_const0x = [And([And(Implies(result[0][j+1] == 1, Or(result[1][j+1] == 1, result[1][j+1] == 0)),
                            Implies(result[0][j+1] == 0, result[1][j+1] == 0))
                        for j in range(4)])]
# formula_const0x1 = [And([Implies(result[i][j+1] == 0, result[i+1][j+1] == 0)
#                       for i in [0] for j in range(4)])]
# 针对非叶子结点的约束
# 对于析取的下放，非叶子结点，当前是1，下面子节点为0或者1，但是至少有一个是1
# 当前不使用formula_const0
# formula_const0 = [And(Implies(result[i][0] == 0, And(result[2*(i+1)-1][0] == 0, result[2*(i+1)][0] == 0)),
#                       Implies(result[i][0] == 1, Or(And(result[2*(i+1)-1][0] == 1, result[2*(i+1)][0] == 0, And([Implies(result[i][j+1] == 1, Or(result[2*(i+1)-1][j+1] == 1, result[2*(i+1)-1][j+1] == 0)) for j in range(4)])),
#                                                     And(result[2*(i+1)][0] == 1, result[2*(i+1)-1][0] == 0, And([Implies(result[i][j+1] == 1, Or(result[2*(i+1)][j+1] == 1, result[2*(i+1)][j+1] == 0)) for j in range(4)])),
#                                                     And(And(result[2*(i+1)-1][0] == 1, And([Implies(result[i][j+1] == 1, Or(result[2*(i+1)-1][j+1] == 1, result[2*(i+1)-1][j+1] == 0)) for j in range(4)])),
#                                                         And(result[2*(i+1)][0] == 1, And([Implies(result[i][j+1] == 1, Or(result[2*(i+1)][j+1] == 1, result[2*(i+1)][j+1] == 0)) for j in range(4)])))))
#                       ) for i in [0]]

# 对于合取的下放，非叶子结点，当前是1，下面的子节点都为1
# 第2个节点的空间下放
formula_const1 = [And([And(Implies(result[1][j+1] == 1, And(Or(result[2][j+1] == 1, result[2][j+1] == 0),
                                                            Or(result[3][j+1] == 1, result[3][j+1] == 0))),
                           Implies(result[1][j+1] == 0, And(result[2][j+1] == 0, result[3][j+1] == 0)))
                       for j in range(4)])]
# 第2、3、4节点的结果上传
formula_const1x = [And(Implies(And(result[2*i][0] == 1, result[2*i+1][0] == 1), result[i][0] == 1),
                      Implies(Or(result[2*i][0] == 0, result[2*i+1][0] == 0), result[i][0] == 0))
                   for i in [1, 2, 3]]
# 对于空间算子的下放，非叶子节点，当前是1，下面的子节点都是1
# formula_const2 = [And(Implies(result[i][0] == 0, And(result[2*(i+1)-1][0] == 0, result[2*(i+1)][0] == 0)),
#                       Implies(result[i][0] == 1, And(result[2*(i+1)-1][0] == 1, result[2*(i+1)][0] == 1,
#                                                      And([Implies(result[i][j+1] == 1, Or(And(result[2*(i+1)-1][j+1] == 1, result[2*(i+1)][j+1] == 0),
#                                                                                       And(result[2*(i+1)-1][j+1] == 0, result[2*(i+1)][j+1] == 1)))
#                                                       for j in range(4)]))))
#                   for i in [1, 2]]
# 第3、4节点的空间下放
formula_const2 = [And([And(Implies(result[2][j+1] == 1, Or(
                And(result[4][j+1] == 1, result[5][j+1] == 0),
                And(result[4][j+1] == 0, result[5][j+1] == 1))), Implies(result[2][j+1] == 0, And(result[4][j+1] == 0, result[5][j+1] == 0))) for j in range(4)])]
formula_const3 = [And([And(Implies(result[3][j+1] == 1, Or(
                And(result[6][j+1] == 1, result[7][j+1] == 0),
                And(result[6][j+1] == 0, result[7][j+1] == 1))), Implies(result[3][j+1] == 0, And(result[6][j+1] == 0, result[7][j+1] == 0))) for j in range(4)])]
# 针对非叶子节点下放约束1的额外补充，空间方位的判断，如果下放前的第一个判断是1的话将约束进行下放
# 对于节点i(值为i-1)的空间约束，判断result[2*(i+1)-1][]和result[2*(i+1)][]之间的关系
# 对于节点2的空间约束，r[i+1][j] == 1表示E
formula_s_x1 = [Or([And(result[4][i+1] == 1, result[5][j+1] == 1, r[i+1][j] == 1) for j in range(4) for i in range(4)])]
# 对于节点3的空间约束，r[i+1][j] == 8表示EN
formula_s_x2 = [Or([And(result[6][i+1] == 1, result[7][j+1] == 1, r[i+1][j] == 8) for j in range(4) for i in range(4)])]

formula_s = formula_s_x1 + formula_s_x2
# 合取和析取下放
# formula_const2 = [And([Implies(result[i][j] == 1, And(Or(result[2*(i+1)-1][j] == 1, result[2*(i+1)-1][j] == 0),
#                                                       Or(result[2*(i+1)][j] == 1, result[2*(i+1)][j] == 0)))
#                       for i in range(1) for j in range(4)])]

# 下放约束3
# formula_const3 = [And([Implies(result[i][j+1] == 0, And(result[2*i][j+1] == 0, result[2*i+1][j+1] == 0))
#                       for i in [1, 2, 3] for j in range(4)])]

con_const = formula_pre + formula_const0x + formula_prex + formula_const1 + formula_const1x + formula_const2 + formula_const3 + formula_s

# /**
#   (5)求解器
# */
s = Solver()
s.add(info_c + con_const + formula_con)
check = s.check()
print(s.check())
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(result[i][j]) for j in range(5)]
         for i in range(8)]
    print_matrix(r)
else:
    print("failed to solve")
