import numpy as np
import os


# 数组生成
# l表示区域数量，v表示变量数量，h表示语法树给出的节点个数
def GenArray(l, v, h):
    s0 = "from z3 import *"
    s1 = "r = [[Int(\"r_%s_%s\" % (i + 1, j + 1)) for j in range(" + str(l) + ")] for i in range(" + str(l + 1) + ")]"
    s2 = "re = [[Int(\"re_%s_%s\" % (i + 1, j + 1)) for j in range(" + str(v) + ")] for i in range(" + str(l + 1) + ")]"
    s3 = "cl = [[Int(\"cl_%s_%s\" % (i + 1, j + 1)) for j in range(" + str(v) + ")] for i in range(" + str(l + 1) + ")]"
    # 只有2列的原因在于第2列只是说明是否为空
    s4 = "fr = [[Int(\"f_%s_%s\" % (i + 1, j + 1)) for j in range(" + str(l) + ")] for i in range(2)]"
    # 只有4个的原因我们默认pth给出的预估路径最长为4个
    s5 = "pth = [[Int(\"p_%s_%s\" % (i + 1, j + 1)) for j in range(4)] for i in range(" + str(v) + ")]"
    s6 = "result = [[Int('x_%d_%d' % (i + 1, j + 1)) for j in range(" + str(l+1) + ")] for i in range(" + str(h) + ")]"
    string_list = np.array([[s0], [s1], [s2], [s3], [s4], [s5], [s6]])
    return string_list


# 数据录入
def AddArray(rx, rex, clx, frx, pthx):
    s1 = "rx = (("
    for i in range(len(rx)):
        for j in range(len(rx[0])):
            s1 = s1 + str(rx[i][j])
            if j != len(rx[0]) - 1:
                s1 = s1 + ", "
        if i != len(rx) - 1:
            s1 = s1 + "), ("
        else:
            s1 = s1 + "))"

    s2 = "rex = (("
    for i in range(len(rex)):
        for j in range(len(rex[0])):
            s2 = s2 + str(rex[i][j])
            if j != len(rex[0]) - 1:
                s2 = s2 + ", "
        if i != len(rex) - 1:
            s2 = s2 + "), ("
        else:
            s2 = s2 + "))"

    s3 = "clx = (("
    for i in range(len(clx)):
        for j in range(len(clx[0])):
            s3 = s3 + str(clx[i][j])
            if j != len(clx[0]) - 1:
                s3 = s3 + ", "
        if i != len(clx) - 1:
            s3 = s3 + "), ("
        else:
            s3 = s3 + "))"

    s4 = "frx = (("
    for i in range(len(frx)):
        for j in range(len(frx[0])):
            s4 = s4 + str(frx[i][j])
            if j != len(frx[0]) - 1:
                s4 = s4 + ", "
        if i != len(frx) - 1:
            s4 = s4 + "), ("
        else:
            s4 = s4 + "))"

    s5 = "pthx = (("
    for i in range(len(pthx)):
        for j in range(len(pthx[0])):
            s5 = s5 + str(pthx[i][j])
            if j != len(pthx[0]) - 1:
                s5 = s5 + ", "
        if i != len(pthx) - 1:
            s5 = s5 + "), ("
        else:
            s5 = s5 + "))"
    string_list = np.array([[s1], [s2], [s3], [s4], [s5]])
    return string_list


# 信息录入约束
def InfoCons(l, v):
    s1 = "info_c1 = [r[i][j] == rx[i][j] for i in range(" + str(l + 1) + ") for j in range(" + str(l) + ")]"
    s2 = "info_c2 = [re[i][j] == rex[i][j] for i in range(" + str(l + 1) + ") for j in range(" + str(v) + ")]"
    s3 = "info_c3 = [cl[i][j] == clx[i][j] for i in range(" + str(l + 1) + ") for j in range(" + str(v) + ")]"
    s4 = "info_c4 = [fr[i][j] == frx[i][j] for i in range(2) for j in range(" + str(l) + ")]"
    s5 = "info_c5 = [pth[i][j] == pthx[i][j] for i in range(" + str(v) + ") for j in range(4)]"
    s6 = "info_c = info_c1 + info_c2 + info_c3 + info_c4 + info_c5"
    string_list = np.array([[s1], [s2], [s3], [s4], [s5], [s6]])
    return string_list


# 叶子节点约束，l表示区域数量，leafList是叶子结点存储的数据，leaf表示叶子节点的id集合
def FormulaLeaf(l, leafList, leaf):
    leaf = map(str, leaf)
    s1 = "formula_rz1 = [And([Implies(And(result[z-1][j + 1] == 1, i != j), result[z-1][i + 1] == 0) " \
         + "for i in range(" + str(l) + ") for j in range(" + str(l) + ")]) for z in [" + ','.join(leaf) + "]]"

    string_list = np.array([[s1]])
    sn = "formula_con = formula_rz1 "
    i = 2
    for key, item1 in leafList.items():
        s2 = ""
        if item1['type_x'] == "re":
            s2 = "formula_rz" + str(i) + " = [And(Implies(Or([And(result[" + str(key - 1) + "][i+1] == 1," \
                 + " re[i+1][" + str(item1['value'] - 101) + "] == 1) for i in range(" + str(l) + ")]), " \
                 + "result[" + str(key - 1) + "][0] == 1), Implies(And([Implies(result[" + str(key - 1) + "]" \
                 + "[i+1] == 1, re[i+1][" + str(item1['value'] - 101) + "] == 0) for i in range(" + str(l) + ")])," \
                 + " result[" + str(key - 1) + "][0] == 0))]"
        if item1['type_x'] == "cl":
            s2 = "formula_rz" + str(i) + " = [And(Implies(Or([And(result[" + str(key - 1) + "][i+1] == 1," \
                 + " cl[i+1][" + str(item1['value'] - 101) + "] == 1) for i in range(" + str(l) + ")]), " \
                 + "result[" + str(key - 1) + "][0] == 1), Implies(And([Implies(result[" + str(key - 1) + "]" \
                 + "[i+1] == 1, cl[i+1][" + str(item1['value'] - 101) + "] == 0) for i in range(" + str(l) + ")])," \
                 + " result[" + str(key - 1) + "][0] == 0))]"
        if item1['type_x'] == "free":
            s2 = "formula_rz" + str(i) + " = [And(Implies(Or([And(result[" + str(key - 1) + "][i+1] == 1," \
                 + " fr[1][i] == 1) for i in range(" + str(l) + ")]), result[" + str(key - 1) + "][0] == 1)," \
                 + " Implies(And([Implies(result[" + str(key - 1) + "][i+1] == 1, fr[1][i] == 0) " \
                 + "for i in range(" + str(l) + ")]), result[" + str(key - 1) + "][0] == 0))]"
        sn = sn + "+ formula_rz" + str(i) + " "
        string_list = np.vstack((string_list, s2))
        i = i + 1
    string_list = np.vstack((string_list, sn))
    return string_list


# 非叶子结点约束，约束下放添加，l表示区域数量，region表示选择需要判断的区域，nodeList表示非叶子结点存储的数据
def FormulaNode(l, region, nodeList):
    # 添加初始约束
    s1 = "formula_pre = [And("
    i = 1
    while i < l:
        s1 = s1 + "result[0][" + str(i) + "] == " + str(region[i - 1]) + ", "
        i = i + 1
    s1 = s1 + "result[0][" + str(l) + "] == " + str(region[l - 1]) + ")]"
    string_list = np.array([[s1]])
    sn = "con_1 = formula_pre "
    snx = "con_2 = [True] "
    sny = "con_3 = [True] "
    # 添加空间下放约束和结果上传
    # 其中formula_const为空间约束的下放，formula_s_x是空间关系的下放，formula_res为空间结果的上传
    i = 1
    j = 1
    for key, item1 in nodeList.items():
        s2 = ""
        s3 = ""
        s4 = ""
        # type_x == 0 表示~， type_x == 1 表示or，type_x == 2 表示and，type_x == 3 表示空间运算符号
        if item1['type_x'] == 0:
            # 空间下放
            s2 = "formula_const" + str(i) + " = [And([And(Implies(result[" + str(key - 1) + "][j+1] == 1, " \
                 + "Or(result[" + str(item1['left'] - 1) + "][j+1] == 1, result[" + str(item1['left'] - 1)\
                 + "][j+1] == 0)), Implies(result[" + str(key - 1) + "][j+1] == 0, " \
                 + "result[" + str(item1['left'] - 1) + "][j+1] == 0)) for j in range(" + str(l) + ")])]"
            # 结果上传
            s4 = "formula_res" + str(i) + " = [And(Implies(result[" + str(item1['left'] - 1) + "][0] == 0," \
                 + " result[" + str(key - 1) + "][0] == 1), Implies(result[" \
                 + str(item1['left'] - 1) + "][0] == 1, result[" + str(key - 1) + "][0] == 0))]"
            string_list = np.vstack((string_list, s2))
            string_list = np.vstack((string_list, s4))
            sn = sn + "+ formula_const" + str(i) + " "
            sny = sny + "+ formula_res" + str(i) + " "
            i = i + 1
        if item1['type_x'] == 1 or item1['type_x'] == 2:
            # 空间下放
            s2 = "formula_const" + str(i) + " = [And([And(Implies(result[" + str(key - 1) + "][j+1] == 1," \
                 + " And(Or(result[" + str(item1['left'] - 1) + "][j+1] == 1, result[" + str(item1['left'] - 1)\
                 + "][j+1] == 0), Or(result[" + str(item1['right'] - 1) + "][j+1] == 1, result[" \
                 + str(item1['right'] - 1) + "][j+1] == 0))), Implies(result[" + str(key - 1) \
                 + "][j+1] == 0, And(result[" + str(item1['left'] - 1) + "][j+1] == 0, result[" \
                 + str(item1['right'] - 1) + "][j+1] == 0))) for j in range(" + str(l) + ")])]"
            # 结果上传
            # type_x == 1 表示or
            if item1['type_x'] == 1:
                s4 = "formula_res" + str(i) + " = [And(Implies(Or(result[" + str(item1['left'] - 1) + "][0] == 1, " \
                    + "result[" + str(item1['right'] - 1) + "][0] == 1), result[" + str(key - 1) + "][0] == 1), " \
                    + "Implies(And(result[" + str(item1['left'] - 1) + "][0] == 0, result[" + str(item1['right'] - 1) \
                    + "][0] == 0), result[" + str(key - 1) + "][0] == 0))]"
            # type_x == 2 表示and
            if item1['type_x'] == 2:
                s4 = "formula_res" + str(i) + " = [And(Implies(And(result[" + str(item1['left'] - 1) + "][0] == 1, " \
                     + "result[" + str(item1['right'] - 1) + "][0] == 1), result[" + str(key - 1) + "][0] == 1), " \
                     + "Implies(Or(result[" + str(item1['left'] - 1) + "][0] == 0, result[" + str(item1['right'] - 1) \
                     + "][0] == 0), result[" + str(key - 1) + "][0] == 0))]"
            string_list = np.vstack((string_list, s2))
            string_list = np.vstack((string_list, s4))
            sn = sn + "+ formula_const" + str(i) + " "
            sny = sny + "+ formula_res" + str(i) + " "
            i = i + 1
        if item1['type_x'] == 3:
            # 空间下放
            s2 = "formula_const" + str(i) + " = [And([And(Implies(result[" + str(key - 1) + "][j+1] == 1, " \
                 + "Or(And(result[" + str(item1['left'] - 1) + "][j+1] == 1, result[" + str(item1['right'] - 1) \
                 + "][j+1] == 0), And(result[" + str(item1['left'] - 1) + "][j+1] == 0, result[" \
                 + str(item1['right'] - 1) + "][j+1] == 1))), Implies(result[" + str(key - 1) \
                 + "][j+1] == 0, And(result[" + str(item1['left'] - 1) + "][j+1] == 0, result[" \
                 + str(item1['right'] - 1) + "][j+1] == 0))) for j in range(" + str(l) + ")])]"
            if GetInt(item1['value']) != 0:
                # 空间关系的下放
                s3 = "formula_s_x" + str(j) + " = [Or([And(result[" + str(item1['left'] - 1) + "][i+1] == 1, result[" \
                     + str(item1['right'] - 1) + "][j+1] == 1, r[i+1][j] == " + str(GetInt(item1['value'])) \
                     + ") for j in range(" + str(l) + ") for i in range(" + str(l) + ")])]"
                # s3 = "formula_s_x" + str(j) + " = [Implies(result[" + str(key - 1) + "][0] == 1, "\
                #      + "Or([And(result[" + str(item1['left'] - 1) + "][i+1] == 1, result[" + str(item1['right'] - 1) \
                #      + "][j+1] == 1, r[i+1][j] == " + str(GetInt(item1['value'])) + ") for j in range(" \
                #      + str(l) + ") for i in range(" + str(l) + ")]))]"
                string_list = np.vstack((string_list, s3))
                snx = snx + "+ formula_s_x" + str(j) + " "
                j = j + 1
            # 结果上传
            s4 = "formula_res" + str(i) + " = [And(Implies(And(result[" + str(item1['left'] - 1) + "][0] == 1, " \
                 + "result[" + str(item1['right'] - 1) + "][0] == 1), result[" + str(key - 1) + "][0] == 1), " \
                 + "Implies(Or(result[" + str(item1['left'] - 1) + "][0] == 0, result[" + str(item1['right'] - 1) \
                 + "][0] == 0), result[" + str(key - 1) + "][0] == 0))]"
            string_list = np.vstack((string_list, s2))
            string_list = np.vstack((string_list, s4))
            sn = sn + "+ formula_const" + str(i) + " "
            sny = sny + "+ formula_res" + str(i) + " "
            i = i + 1
    sn = sn + "+ con_2 + con_3"
    string_list = np.vstack((string_list, snx, sny, sn))
    return string_list


# 返回1-8对应的值，1-8 ::= E,ES,S,WS,W,WN,N,EN
def GetInt(a):
    if a == 'E':
        return 1
    if a == 'ES':
        return 2
    if a == 'S':
        return 3
    if a == 'WS':
        return 4
    if a == 'W':
        return 5
    if a == 'WN':
        return 6
    if a == 'N':
        return 7
    if a == 'EN':
        return 8
    return 0


def GetStr(a):
    if a == 1:
        return 'E'
    if a == 2:
        return 'ES'
    if a == 3:
        return 'S'
    if a == 4:
        return 'WS'
    if a == 5:
        return 'W'
    if a == 6:
        return 'WN'
    if a == 7:
        return 'N'
    if a == 8:
        return 'EN'
    return ''


# 生成求解器
def GenSolver(l, h):
    s1 = "s = Solver()"
    s2 = "s.add(info_c + con_1 + formula_con)"
    s3 = "check = s.check()"
    s4 = "print(s.check())"
    s5 = "if s.check() == sat:"
    s6 = "    m = s.model()"
    s7 = "    r = [[m.evaluate(result[i][j]) for j in range(" + str(l + 1) + ")] for i in range(" + str(h) + ")]"
    s8 = "    print_matrix(r)"
    s9 = "else:"
    s10 = "    print(\"failed to solve\")"
    string_list = np.array([[s1], [s2], [s3], [s4], [s5], [s6], [s7], [s8], [s9], [s10]])
    return string_list


# 写之前，先检验文件是否存在，存在就删掉
if os.path.exists("dest.txt"):
    os.remove("dest.txt")

rx = ((1, 2, 3, 4),
      (0, 1, 1, 8),
      (5, 0, 1, 8),
      (5, 5, 0, 8),
      (4, 4, 4, 0))

rex = ((101, 102),
       (0, 0),
       (1, 0),
       (0, 0),
       (0, 1))

clx = ((101, 102),
       (0, 0),
       (0, 0),
       (0, 1),
       (0, 0))

frx = ((1, 2, 3, 4),
       (1, 0, 0, 0))

pthx = ((2, 1, 0, 0),
        (4, 3, 2, 1))

# leafList = {
#     5: {
#         'type_x': "re",
#         'value': 101
#     },
#     6: {
#         'type_x': "re",
#         'value': 101
#     },
#     7: {
#         'type_x': "re",
#         'value': 101
#     },
#     8: {
#         'type_x': "re",
#         'value': 102
#     },
#     9: {
#         'type_x': "free",
#         'value': 101
#     }
# }

leafList = {
    5: {
        'type_x': 're',
        'value': 101,
        'truth': 1},
    6: {
        'type_x': 'cl',
        'value': 102,
        'truth': 1},
    7: {
        'type_x': 're',
        'value': 101,
        'truth': 1},
    8: {
        'type_x': 're',
        'value': 102,
        'truth': 1}
}


nodeList = {
    1: {
        'type_x': 0,
        'value': '~',
        'left': 2,
        'right': -1},
    2: {
        'type_x': 2,
        'value': 'And',
        'left': 3,
        'right': 4},
    3: {
        'type_x': 3,
        'value': 'E',
        'left': 5,
        'right': 6},
    4: {
        'type_x': 3,
        'value': 'EN',
        'left': 7,
        'right': 8}
}

leaf = [5,6,7,8]

region = [0, 1, 1, 1]

# nodeList = {
#     1: {
#         'type_x': 2,
#         'value': ''
#     },
#     2: {
#         'type_x': 1,
#         'value': ''
#     },
#     3: {
#         'type_x': 2,
#         'value': ''
#     },
#     4: {
#         'type_x': 3,
#         'value': 'S'
#      }
# }

# l区域数量, v变量数量, h语法树节点个数, leafS叶子结点起始位置, leafE叶子结点结束位置, nodeE非叶子结点结束位置
l = 4
v = 2
h = 8

mylist = np.vstack((
                   GenArray(l, v, h), AddArray(rx, rex, clx, frx, pthx), InfoCons(l, v), FormulaLeaf(l, leafList, leaf),
                   FormulaNode(l, region, nodeList), GenSolver(l, h)))

# 以写的方式打开文件，如果文件不存在，就会自动创建
file_write_obj = open("dest.txt", 'w')
for var in mylist:
    file_write_obj.writelines(var)
    file_write_obj.write('\n')
file_write_obj.close()
