# transactions
import time
from functools import wraps
from memory_profiler import profile
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

# filename = "F:/PycharmFile/data_mining_project/data/test_data.data"
filename = "F:/PycharmFile/data_mining_project/data/T10L10I10.data"
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



def first_set(result_dataset):
    itemSet = []
    for transaction in result_dataset:
        for item in transaction:
            if [item] not in itemSet:
                itemSet.append([item])  # generate f-1 set
    itemSet.sort()
    # print(itemSet)
    return itemSet



def support_counting(dataset, itemset_candidate):
    map_dataset = map(set, dataset)
    sset = {}

    for trans in map_dataset:
        for item in map(frozenset, itemset_candidate):
            if len(item) > len(trans):
                continue
            else:
                if item.issubset(trans):
                    sset[item] = sset.get(item, 0) + 1
                else:
                    sset[item] = sset.get(item, 0)

            # if item.issubset(trans):
            #     sset[item] = sset.get(item, 0) + 1
            # else:
            #     sset[item] = sset.get(item, 0)
    # print(sset)
    itemsnum = len(dataset)

    return itemsnum, sset


def prunning(dataset, itemset_candidate):
    itemsnum, sset = support_counting(dataset, itemset_candidate)
    misup = 0.1
    list_frequent = []
    support_all = {}   # 字典键值对
    for key in sset:
        support = sset[key]
        # print(key, support)
        if support >= misup*itemsnum:
            list_frequent.insert(0, key)
            # print(key)
            support_all[key] = support
    print(support_all)
    return list_frequent, support_all



# print("frequentItem:", frequentList[0])
# print(len(frequentList))
# listffff = list(frequentList[0])
# print(listffff)
# listdsa = [[2, 3, 2], [1], [2], [3], [4]]
# selist = []
#
# for key in map(frozenset, listdsa):
#     print(key)
#     selist.insert(0, key)
#
# print(list(selist[4])[0:2])

def candidate_generation(item_list, k):
    candidatelist = []
    for i in range(len(item_list)):
        for j in range(i + 1, len(item_list)):
            listA = list(item_list[i])[:k - 2]
            listB = list(item_list[j])[:k - 2]
            # listAlast = list(item_list[i])[k-2]
            # listBlast = list(item_list[j])[k-2]
            listA.sort()
            listB.sort()
            # if (listA == listB) and (listAlast != listBlast):  #并不会有重复的
            if listA == listB:
                candidatelist.append(item_list[i] | item_list[j])

    # print(candidatelist)
    return candidatelist


def apriori(dataset):
    k = 2
    itemSet = first_set(dataset)
    resultset = []
    c_g_time = 0
    s_c_time = 0
    frelist_aftercount, result = prunning(dataset, itemSet)
    resultset.append(result)
    # print("frequentList:", frelist_aftercount)
    while len(frelist_aftercount) > 0:
        t0 = time.time()
        frequentList = candidate_generation(frelist_aftercount, k)
        t1 = time.time()
        frelist_aftercount, result = prunning(dataset, frequentList)
        t2 = time.time()
        resultset.append(result)
        # print(frequentList)
        # print(len(frequentList))
        # print(frelist_aftercount)
        # print(len(frelist_aftercount))
        k = k + 1
        c_g_time = c_g_time + (t1 - t0)
        s_c_time = s_c_time + (t2 - t1)
    print(resultset)
    print('c_g_time', c_g_time)
    print('s_c_time', s_c_time)

    return 0

@profile
def run():
    res = read_datafile(filename)
    apriori(res)


cProfile.run("run()")