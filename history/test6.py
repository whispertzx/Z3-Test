from z3 import *

# /**
#   (1)转化前步骤
#   (2)信息约束
#   (3)初始行约束和原子公式行约束[将公式中每个节点根据节点下放约束(3)将条件加入result集合中]
#   (4)节点下放约束[将公式中第一行初始化条件和原子公式所在的叶子节点行所在约束(4)加入result集合中]
#   (5)求解器构建和结果输出
# */

# /**
#   (1)转化前步骤
#   1、我们根据输入的逻辑公式构造语法树，给出语法树的节点个数，其中not符号下放到原子公式中
#   2、将逻辑公式中的：F B L R LF LB RF RB根据当前主车辆的行驶方向，将其转化为 E,ES,S,WS,W,WN,N,EN
# */

r = [[Int("r_%s_%s" % (i+1, j+1)) for j in range(4)]
     for i in range(5)]

re = [[Int("re_%s_%s" % (i+1, j+1)) for j in range(2)]
      for i in range(5)]

cl = [[Int("cl_%s_%s" % (i+1, j+1)) for j in range(2)]
      for i in range(5)]

fr = [[Int("f_%s_%s" % (i+1, j+1)) for j in range(4)]
      for i in range(2)]

dir = [[Int("d_%s_%s" % (i+1, j+1)) for j in range(2)]
       for i in range(2)]

pth = [[Int("p_%s_%s" % (i+1, j+1)) for j in range(4)]
       for i in range(3)]

# 定义带求解的返回数组result
result = [[Int('x_%d_%d' % (i + 1, j + 1)) for j in range(4)]
          for i in range(5)]

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

# 第二步：录入区域性质，维护状态信息表，共n张（n根据实际使用的性质来判定，例如re、cl、free共3张）
# 第一行表示物体编号，分别用100-110表示，第2行起行表示区域，列表示物体
# example:[其中1表示在列，0表示不在列]
rex = ((101, 102),
       (0,    0),
       (1,    0),
       (0,    0),
       (0,    1))
# example:[其中1表示在列，0表示不在列]
clx = ((101, 102),
       (0,    0),
       (0,    0),
       (0,    1),
       (0,    0))
# example:[其中1表示在列，0表示不在列]
frx = ((1, 2, 3, 4),
       (1, 0, 0, 0))

# 第三步：录入车辆的行驶方向表，共1张，1-8 ::= E,ES,S,WS,W,WN,N,EN
# example:
dirx = ((101, 102),
        (1,    4))

# 第四步：录入车辆pth表，默认路径长度最大为4，共1张
# example:[第二行起的数字为区域的编号]
pthx = ((1, 2, 3, 4),
        (2, 1, 0, 0),
        (4, 3, 2, 1))

# 信息录入约束
info_c1 = [r[i][j] == rx[i][j] for i in range(5) for j in range(4)]
info_c2 = [re[i][j] == rex[i][j] for i in range(5) for j in range(2)]
info_c3 = [cl[i][j] == clx[i][j] for i in range(5) for j in range(2)]
info_c4 = [fr[i][j] == frx[i][j] for i in range(2) for j in range(4)]
info_c5 = [dir[i][j] == dirx[i][j] for i in range(2) for j in range(2)]
info_c6 = [pth[i][j] == pthx[i][j] for i in range(3) for j in range(4)]

info_c = info_c1 + info_c2 + info_c3 + info_c4 + info_c5 + info_c6

# /**
#   (3)初始行约束和原子公式行约束
# */
# 对于结果集我们构造一个表，让求解空间划分问题变成寻找这一张表能不能完成类似数独问题的一个解
# 构建一个行数等同于语法树节点数量的结果集，其中列长度等同于区域长度
# example1: 例如公式re(101) B cl(102)，树有3个节点，因此result集有3行
#          B
#      /      \
#  re(101)  cl(102)

# example2: 例如公式(re(101) B cl(102)) and (re(101) LB re(102))，result集仍为3个，
#           相当于我们分别输入re(101) B cl(102) 和 re(101) LB re(102)，如果都成立，则返回成立
#          B                 LB
#      /      \           /      \
#  re(101)  cl(102)   re(101)   re(102)
#
#                       and
#                /              \
#              B                  LB
#           /     \            /      \
#       re(101)  cl(102)   re(101)  re(102)


# example3: 例如公式（re(101) B cl(102)） LB re(102)，
#                LB
#             /     \
#           B     re(102)
#        /    \
#   re(101)  cl(102)

# 例如在给定的2个区域内，那么我们需要添加约束至这张result集，对于不属于该区域的列强制为0，对于结果集，第2、3行的结果受限于第1行，i行约束了2i和2i+1
# 一开始，我们要显示的指定遍历result的行数范围大小为n，获得叶子结点的个数n0 <=> n - n2 <=> (n + 1)/2   n2 = (n - 1)/2

# 公式约束，例如result中的第z行满足原子公式re(x)、cl(x)、free
# formula_rz1 = [And([Implies(And(result[z][j] == 1, i != j), result[z][i] == 0) for i in range(4) for j in range(4)])]
# formula_rz2 = [Or([And(result[z][i] == 1, re[i+1][x-101] == 1) for i in range(4)])]
# formula_rz3 = [Or([And(result[z][i] == 1, cl[i+1][x-101] == 1) for i in range(4)])]
# formula_rz4 = [Or([And(result[z][i] == 1, free[1][i] == 1) for i in range(4)])]
# con_rex = formula_rz1 + formula_rz2
# con_clx = formula_rz1 + formula_rz3
# con_free = formula_rz1 + formula_rz4

# /**
#   --------------
#   实例测试
#   example3
#   --------------
# */
# 针对example3我们给出具体的约束下放实例(re(101) B cl(102)) LB re(102)，给定区域如果为2，3，4(结果应该返回sat)
# 初始约束，判断的区域范围
formula_pre = [And(result[0][0] == 0, result[0][1] == 1, result[0][2] == 1, result[0][3] == 1)]

# 针对非叶子结点的约束
# 这边我们首先将公式修改为使用绝对方位的判断值：(re(101) E cl(102)) EN re(102)
# 对于节点1和2，我们使用下放约束1
formula_const1 = [And([Implies(result[i][j] == 1, Or(
                And(result[2*(i+1)-1][j] == 1, result[2*(i+1)][j] == 0),
                And(result[2*(i+1)-1][j] == 0, result[2*(i+1)][j] == 1))) for i in range(2) for j in range(4)])]
# 针对非叶子节点下放约束1的额外补充，空间方位的判断
# 对于节点i(值为i-1)的空间约束，判断result[2*(i+1)-1][]和result[2*(i+1)][]之间的关系
# 对于节点1的空间约束，r[i+1][j] == 8表示EN
formula_s_x1 = [Or([And(result[1][i] == 1, result[2][j] == 1, r[i+1][j] == 8) for j in range(4) for i in range(4)])]
# 对于节点2的空间约束，r[i+1][j] == 1表示E
formula_s_x2 = [Or([And(result[3][i] == 1, result[4][j] == 1, r[i+1][j] == 1) for j in range(4) for i in range(4)])]

formula_s = formula_s_x1 + formula_s_x2
# 不存在合取和析取下放
formula_const2 = [True]
# 下放约束3
formula_const3 = [And([Implies(result[i][j] == 0, And(result[2*(i+1)-1][j] == 0, result[2*(i+1)][j] == 0))
                      for i in range(2) for j in range(4)])]

con_const = formula_pre + formula_const1 + formula_const2 + formula_const3 + formula_s

# 针对叶子节点的约束，依次对应即可
# 基本约束，原子公式区域为1
formula_rz1 = [And([Implies(And(result[z+2][j] == 1, i != j), result[z+2][i] == 0)
                    for z in range(3) for i in range(4) for j in range(4)])]
# 对于节点3的约束，节点3为re(102)
formula_rz2 = [Or([And(result[2][i] == 1, re[i+1][102-101] == 1) for i in range(4)])]
# 对于节点4的约束，节点4为re(101)
formula_rz3 = [Or([And(result[3][i] == 1, re[i+1][101-101] == 1) for i in range(4)])]
# 对于节点5的约束，节点5为cl(102)
formula_rz4 = [Or([And(result[4][i] == 1, cl[i+1][102-101] == 1) for i in range(4)])]

formula_con = formula_rz1 + formula_rz2 + formula_rz3 + formula_rz4

# /**
#   (4)节点下放约束
# */
# 下放约束1：空间关系算子符号下放，其中i的编号应该被指定
# formula_const1 = [And([Implies(result[i][j] == 1, Or(
#                 And(result[2*(i+1)-1][j] == 1, result[2*(i+1)][j] == 0),
#                 And(result[2*(i+1)-1][j] == 0, result[2*(i+1)][j] == 1))) for i in range(n0) for j in range(4)])]
# 下放约束2：合取和析取下放，其中i的编号应该被指定[此处规定合取和析取的结果是直接统一至下层]
# formula_const2 = [And([And(result[i][j] == result[2*(i+1)-1][j], result[i][j] == result[2*(i+1)][j])
#                       for i in range(n0) for j in range(4)])]
# 下放约束2：合取和析取下放，其中i的编号应该被指定[此处规定合取和析取的结果可以缺失一部分r进行下沉]
# formula_const2 = [And([And(result[i][j] == 1, Or(result[2*(i+1)-1][j] == 1, result[2*(i+1)-1][j] == 0),
#                            Or(result[2*(i+1)][j] == 1, result[2*(i+1)][j] == 0))
#                       for i in range(n0) for j in range(4)])]
# 下放约束3：区域不被标记使用，则在后续的判定中也不会被指定，其中n0通过总节点长度计算得出：n0 = (n + 1)/2
# formula_const3 = [And([Implies(result[i][j] == 0, And(result[2*(i+1)-1][j] == 0, result[2*(i+1)][j] == 0))
#                       for i in range(n0) for j in range(4)])]
# 下放约束1——空间约束：对于节点i(值为i-1)的空间约束
# 判断result[2*(i+1)-1][]和result[2*(i+1)-1][]之间的关系，其中p ::= 1-8 <=> E,ES,S,WS,W,WN,N,EN
# formula_s_xi = [Or([And(result[2*(i+1)-1][i] == 1, result[2*(i+1)-1][j] == 1, r[i+1][j] == p)
#                     for j in range(4) for i in range(4)])]
# con_const = formula_const1 + formula_const2 + formula_const3 + formula_s_xi

# /**
#   (5)求解器
# */
s = Solver()
s.add(info_c + con_const + formula_con)
check = s.check()
print(s.check())
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(result[i][j]) for j in range(4)]
         for i in range(5)]
    print_matrix(r)
else:
    print("failed to solve")
