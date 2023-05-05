import re


def indexStr(sn, s):
    # 给定空列表，将结果值写入此列表中
    res = []
    for i in range(sn.count(s)):
        if i == 0:
            pos = sn.index(s)
        else:
            pos = sn.index(s, pos + 1)
        res.append(pos)
    return res


def splitStr(s):
    # 简易处理，依据空格进行划分
    # ((~re(a3) (F|B) re(b))) %% re(a) F free F cross And re(a) LF re(a1) %% re(a) F ((cross And ~cl(a))) And re(a) F free
    pre = s.split(" ")
    res = []
    for item in pre:
        if item is not "(" and len(indexStr(item, "(")) > len(indexStr(item, ")")):
            list_i = indexStr(item, "(")
            j = 0
            if len(indexStr(item, ")")) == 0:
                for i in range(len(list_i)):
                    res.append(item[j:list_i[i] + 1])
                    j = list_i[i] + 1
                res.append(item[j:])
            else:
                for i in range(len(list_i) - 1):
                    if list_i[i] == list_i[i + 1] - 1:
                        res.append(item[list_i[i]:list_i[i] + 1])
                        j = list_i[i] + 1
                    else:
                        res.append(item[j:list_i[i] + 1])
                        j = list_i[i] + 1

                    if i == len(list_i) - 2:
                        res.append(item[j:])
        elif item is not ")" and len(indexStr(item, ")")) > len(indexStr(item, "(")):
            list_i = indexStr(item, ")")
            if len(indexStr(item, "(")) == 0:
                for i in range(len(list_i)):
                    if i == 0:
                        res.append(item[:list_i[i]])
                        res.append(item[list_i[i]:list_i[i] + 1])
                    else:
                        res.append(item[list_i[i]:list_i[i] + 1])
            else:
                for i in range(len(list_i) - 1):
                    if i == 0:
                        res.append(item[:list_i[i] + 1])
                        res.append(item[list_i[i] + 1:list_i[i + 1] + 1])
                    else:
                        res.append(item[list_i[i] + 1:list_i[i + 1] + 1])
        else:
            res.append(item)
    return res


def strCheck(s):
    for item in s:
        if item == "(" or item == ")" or item == "And" or item == "Or":
            print(1)
        elif re.match(r"^[~]?(F|B|L|R|LF|LB|RF|RB)$", item) is not None:
            print(2)
        # elif item == "F" or item == "~F" or item == "B" or item == "~B" or item == "L" or item == "~L":
        #     print(2)
        # elif item == "R" or item == "~R" or item == "LF" or item == "~LF" or item == "LB" or item == "~LB":
        #     print(2)
        # elif item == "RF" or item == "~RF" or item == "RB" or item == "~RB":
        #     print(2)
        elif re.match(r"^[~]?\([(F|B|L|R|LF|LB|RF|RB)|]+(F|B|L|R|LF|LB|RF|RB)\)$", item) is not None:
            print(3)
        elif re.match(r"^[~]?re\([a-z]{1}[0-9]{0,1}\)$", item) is not None:
            print(4)
        elif re.match(r"^[~]?cl\([a-z]{1}[0-9]{0,1}\)$", item) is not None:
            print(5)
        elif re.match(r"^[~]?free$", item) is not None or re.match(r"^[~]?cross$", item) is not None:
            print(6)
        else:
            return item
    return "True"


if __name__ == '__main__':
    string = input('请输入一个字符串:')
    result = splitStr(string)
    print(result)
    if strCheck(result) is not "True":
        print("There may be a error occur at " + strCheck(result) + " in syntax \"" + string + "\"")
    else:
        print(result)
