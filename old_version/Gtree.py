# coding:UTF8
import graphviz
from Scheck import *


class TNode:
    def __init__(self, x):
        self.val = x
        self.id = None
        self.left = None
        self.right = None


class Solution:
    # 判断是否是运算符
    def isOper(self, ch):
        if ch == "(" or ch == ")" or ch == "And" or ch == "Or":
            return True
        elif re.match(r"^[~]?\([(F|B|L|R|LF|LB|RF|RB)|]+(F|B|L|R|LF|LB|RF|RB)\)$", ch) is not None or re.match(r"^[~]?(F|B|L|R|LF|LB|RF|RB)$", ch) is not None:
            return True
        return False

    # 获取运算符所对应的优先级别
    def getOperOrder(self, ch):
        if ch == '(':
            return 1
        if ch in ['And', 'Or']:
            return 2
        if re.match(r"^[~]?\([(F|B|L|R|LF|LB|RF|RB)|]+(F|B|L|R|LF|LB|RF|RB)\)$", ch) is not None or re.match(r"^[~]?(F|B|L|R|LF|LB|RF|RB)$", ch) is not None:
            return 3
        return 0

    # 中序遍历表达式二叉树
    def InorderTree(self, pNode):
        if not pNode:
            return
        if pNode.left:
            # 如果左子树是符号，且优先级低于父节点的优先级则需要加括号
            if self.isOper(pNode.left.val) and self.getOperOrder(pNode.left.val) < self.getOperOrder(pNode.val):
                res.append('(')
                self.InorderTree(pNode.left)
                res.append(')')
            else:
                self.InorderTree(pNode.left)
        res.append(pNode.val)
        if pNode.right:
            # 如果有子树是符号且优先级低于父节点的优先级，则需要加括号
            if self.isOper(pNode.right.val) and self.getOperOrder(pNode.right.val) <= self.getOperOrder(pNode.val):
                res.append('(')
                self.InorderTree(pNode.right)
                res.append(')')
            else:
                self.InorderTree(pNode.right)

    # 创建二叉树
    def createTree(self, data):
        if not data:
            return
        ch = data.pop(0)
        if ch == '#':
            return None
        else:
            root = TNode(ch)
            root.left = self.createTree(data)
            root.right = self.createTree(data)
            return root

    # 后缀表达式生成二叉树
    def PostExpTree(self, data):
        if not data:
            return
        rep = []
        while data:
            tmp = data.pop(0)
            if not self.isOper(tmp):
                rep.append(TNode(tmp))
            else:
                p = TNode(tmp)
                p.right = rep.pop()
                p.left = rep.pop()
                rep.append(p)
        return rep.pop()

    # 前缀表达式生成二叉树
    def PreExpTree(self, data):
        rep = []
        while data:
            tmp = data.pop()
            if not self.isOper(tmp):
                rep.append(TNode(tmp))
            else:
                p = TNode(tmp)
                p.left = rep.pop()
                p.right = rep.pop()
                rep.append(p)
        return rep.pop()

    # 中缀表达式生成二叉树
    def InExpTree(self, data):
        rep = []
        op = []
        while data:
            tmp = data.pop(0)
            if not self.isOper(tmp):
                rep.append(tmp)
            else:
                if tmp == '(':
                    op.append('(')
                elif tmp == ')':
                    while op[-1] != '(':
                        rep.append(op.pop())
                    op.pop()
                elif re.match(r"^[~]?\([(F|B|L|R|LF|LB|RF|RB)|]+(F|B|L|R|LF|LB|RF|RB)\)$", tmp) is not None or re.match(r"^[~]?(F|B|L|R|LF|LB|RF|RB)$", tmp) is not None or tmp == "And" or tmp == "Or":
                    while op and op[-1] != '(' and self.getOperOrder(op[-1]) >= self.getOperOrder(tmp):
                        rep.append(op.pop())
                    op.append(tmp)
        if op:
            rep = rep + op[::-1]
        print(rep)
        return self.PostExpTree(rep)


# 层序遍历树，将各个节点按顺序进行标记
def levelTree(root):
    if not root:
        return
    queue = [root]
    i = 1
    while queue:
        size = len(queue)
        for _ in range(size):
            node = queue.pop(0)
            node.id = i
            i = i + 1
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return root


# 前序递归遍历各个节点，使用levelTree生成的唯一id来作为节点的编号，将val作为label值进行显示
def tree_to_dot(root, dot):
    if not root:
        return
    dot.node(str(root.id), label=str(root.val))
    if root.left:
        dot.edge(str(root.id), str(root.left.id))
        tree_to_dot(root.left, dot)
    if root.right:
        dot.edge(str(root.id), str(root.right.id))
        tree_to_dot(root.right, dot)


# 生成dot文件，并存储到img文件夹下进行保存，名为tree.png
def draw_tree(root):
    dot = graphviz.Digraph(comment='Binary Tree')
    tree_to_dot(root, dot)
    dot.format = 'png'
    dot.render('tree', 'img')


# 层序遍历的方式将生成的语法树划分为非叶子节点列表nodeList和叶子结点列表leafList
# 同时给出对应的nodeList映射到的子节点的下标
def con_tree_list(root):
    if not root:
        return
    queue = [root]
    nodelist = {}
    nodeindex = {}
    leaflist = {}
    while queue:
        size = len(queue)
        for _ in range(size):
            node = queue.pop(0)
            if node.left and node.right:
                nodeindex[node.id] = {
                        'left': node.left.id,
                        'right': node.right.id
                }
                if Solution.getOperOrder(node.val, node.val) == 2 and node.val == "Or":
                    nodelist[node.id] = {
                        'type_x': 1,
                        'value': ''}
                elif Solution.getOperOrder(node.val, node.val) == 2 and node.val == "And":
                    nodelist[node.id] = {
                        'type_x': 2,
                        'value': ''}
                elif Solution.getOperOrder(node.val, node.val) == 3:
                    nodelist[node.id] = {
                        'type_x': 1,
                        'value': node.val}
            else:
                m = ""
                x = ""
                if "free" in node.val:
                    m = "free"
                elif "cl" in node.val:
                    m = "cl"
                    x = re.findall(r'\((.*?)\)', node.val)[0]
                elif "re" in node.val:
                    m = "re"
                    x = re.findall(r'\((.*?)\)', node.val)[0]
                elif "cross" in node.val:
                    m = "cross"
                if "~" in node.val:
                    n = 0
                else:
                    n = 1
                leaflist[node.id] = {
                    'type_x': m,
                    'value': x,
                    'truth': n}
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return nodelist, leaflist, nodeindex


if __name__ == '__main__':
    string = input('请输入一个字符串:')
    result = splitStr(string)
    print(result)
    if strCheck(result) is not "True":
        print("There may be a error occur at " + strCheck(result) + " in syntax \"" + string + "\"")
    else:
        print(result)
        s = Solution()
        t1 = s.InExpTree(result)
        t1 = levelTree(t1)
        nodelist, leaflist, nodeindex = con_tree_list(t1)
        res = []
        draw_tree(t1)
        s.InorderTree(t1)
        res = map(str, res)
        print(''.join(res))
        print(nodelist)
        print(leaflist)
        print(nodeindex)
