# Fp-growth
import time
from functools import wraps
from memory_profiler import profile, memory_usage
import cProfile


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" %
              (function, str(t1 - t0))
              )
        return result

    return function_timer


class FPtree:

    def __init__(self, name, num, parentNode):
        self.name = name
        self.count = num
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, num):
        self.count += num

    def disp(self, ind=1):
        print(' ' * ind, self.name, self.count)  # * 是乘号的意思
        for child in self.children.values():
            child.disp(ind + 1)

    def disp_all(self, ind=1):
        # print('p:', self.parent, 'n:', self.name, 'c:', self.children)
        print('p:', self.parent, 'n:', self.name, 'link:', self.count)  # 只看parent
        for child in self.children.values():
            child.disp_all(ind + 1)


# rootNode = FPtree('node1', 2, None)
# rootNode.children['node3'] = FPtree('node3', 1, 'node1')
# rootNode.children['node4'] = FPtree('node4', 3, 'node1')
# rootNode.disp_all()

# filename = "F:/PycharmFile/data_mining_project/data/data.txt"
# filename = "F:/PycharmFile/data_mining_project/data/T10I4D100K.data"
# filename = "F:/PycharmFile/data_mining_project/data/test_data.data"

filename = "F:/PycharmFile/data_mining_project/data/T1L10I10.data"


# T1L10I10
# T10L10I10
# T100L10I10
# T10L10I1
# T10L10I10
# T10L10I100
# T10L10I10
# T10L20I10
# T10L50I10


def read_datafile(file):
    result = []
    fd = open(file, "r")
    for line in fd.readlines():
        linestr = line.strip()
        # print(linestr)
        linestrlist = linestr.split(' ')
        del linestrlist[0:2]  # delete first two index
        # print(linestrlist)
        linelist = map(int, linestrlist)
        # print(linelist)
        result.append(list(linelist))
        # result.append(list(map(int, line.split(','))))
    # print(result)
    fd.close()
    return result


def creat_fptree(res):
    minsup = 0.006
    dataset = []
    for key in map(frozenset, res):
        dataset.insert(0, key)  # 生成不可变的集合
    headerDict = {}  # 集合可有元素名:元素值
    freqHeaderDict = {}
    for trans in dataset:
        for item in trans:  # 每个item都是可取的 trans = frozenset({1, 2, 3, 5}),, item = 1,2,3,5
            headerDict[item] = headerDict.get(item, 0) + 1  # 生成头指针列表
    itemsnum = len(dataset)
    # print(itemsnum)
    # print('headerDict', headerDict)
    for key in headerDict:
        support = headerDict[key]  # 去除不满足misup的元素
        if support >= minsup * itemsnum:
            freqHeaderDict[key] = headerDict[key]
    # print('freqHeaderDict', freqHeaderDict)

    # sortFreqHeaderDict = sorted(freqHeaderDict.items(), key=lambda d: d[1], reverse=True)  # 总体排序
    # print(sortFreqHeaderDict)
    # print(headerDict[0][0])
    for k in freqHeaderDict:
        freqHeaderDict[k] = [freqHeaderDict[k], None]

    fptree = FPtree('null', 1, None)

    for trans in dataset:
        freqTans = {}
        for item in trans:
            if item in freqHeaderDict:
                freqTans[item] = freqHeaderDict[item][0]  # 看原始trans是否频繁
        if len(freqTans) > 0:
            orderedItems = [i[0] for i in sorted(freqTans.items(), key=lambda d: d[1], reverse=True)]  # 排序
            # i[0] for i in #means 只取出元组的第一项item name, trans排序
            # print('orderedItems', orderedItems)
            treegrowth(orderedItems, fptree, freqHeaderDict)
    return fptree, freqHeaderDict


def treegrowth(itemtrans, fptree, header):
    if itemtrans[0] in fptree.children:
        fptree.children[itemtrans[0]].inc(1)  # count = 1
    else:
        fptree.children[itemtrans[0]] = FPtree(itemtrans[0], 1, fptree)
        if header[itemtrans[0]][1] == None:
            header[itemtrans[0]][1] = fptree.children[itemtrans[0]]
        else:
            updateheader(header[itemtrans[0]][1], fptree.children[itemtrans[0]])
    if len(itemtrans) > 1:
        treegrowth(itemtrans[1::], fptree.children[itemtrans[0]], header)


def updateheader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):  # 只要是当前节点的nodelink不为空，就替换为到指向的节点，一直到尾节点
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


#
def generate_prefix(header):
    # prefixSet = {}

    prefixList = []
    # print('header:', header)
    branch = header
    bag = header
    while bag:
        # print('###')
        subPreficList = []
        while branch.parent:  # 当其不等于none
            # print(branch.name)
            subPreficList.insert(0, branch.name)
            branch = branch.parent
        # if len(subPreficList) > 1:
        subPreficList.pop()

        # if bag.count*subPreficList
        for i in range(bag.count):
            prefixList.append(subPreficList)
        bag = bag.nodeLink
        branch = bag
        # print(prefixList)

    # prefixSet[item] = prefixList

    # print('prefixList:', prefixList)
    return prefixList


def mine_freq(header, prefix, freqlist):
    pattern = [v[0] for v in sorted(header.items(), key=lambda p: p[1][0], reverse=True)]
    # print('pattern:', pattern)
    for i in range(len(pattern) - 1, -1, -1):  # 逆序取最后一个元素
        ip = pattern[i]
        newfreqset = prefix.copy()
        newfreqset.add(ip)
        freqlist.append(newfreqset)
        # print('ip:################################################', ip)

        prefixSet = generate_prefix(header[ip][1])
        fptree, freqHeader = creat_fptree(prefixSet)

        if freqHeader != None:
            mine_freq(freqHeader, newfreqset, freqlist)

@profile
def run():
    t = time.time()
    res = read_datafile(filename)

    t0 = time.time()
    fptree2, freqHeaderDict = creat_fptree(res)
    t1 = time.time()
    freqItems = []

    mine_freq(freqHeaderDict, set([]), freqItems)
    t2 = time.time()
    # print('read file running time:', (t0 - t))
    # print('creat_fptree running time:', (t1 - t0))
    # print('mine_freq running time:', (t2 - t1))
    # print('generate_prefix running time:')
    # print('total running time:', (t2 - t))

    print(freqItems)

# run()
cProfile.run("run()")