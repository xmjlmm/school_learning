
# Importing required modules
import math
import random
import matplotlib.pyplot as plt


# First function to optimize
def function1(x):
    value = -x ** 2
    return value


# Second function to optimize
def function2(x):
    value = -(x - 2) ** 2
    return value


# Function to find index of list,且是找到的第一个索引
def index_of(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


# Function to sort by values 找出front中对应值的索引序列
def sort_by_values(list1, values):
    sorted_list = []
    while (len(sorted_list) != len(list1)):
        if index_of(min(values), values) in list1:
            sorted_list.append(index_of(min(values), values))
        values[index_of(min(values), values)] = math.inf
    return sorted_list


# Function to carry out NSGA-II's fast non dominated sort
def fast_non_dominated_sort(values1, values2):
    S = [[] for i in range(0, len(values1))]  # len(values1)个空列表
    front = [[]]
    n = [0 for i in range(0, len(values1))]
    rank = [0 for i in range(0, len(values1))]
    # 将front0全部整理出来了，并未对front1-n等进行整理
    for p in range(0, len(values1)):
        S[p] = []
        n[p] = 0
        for q in range(0, len(values1)):
            if (values1[p] > values1[q] and values2[p] > values2[q]) or (
                    values1[p] >= values1[q] and values2[p] > values2[q]) or (
                    values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] > values1[p] and values2[q] > values2[p]) or (
                    values1[q] >= values1[p] and values2[q] > values2[p]) or (
                    values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
    i = 0
    # 该循环能将所有的个体全部进行分类，显然最后一层的个体中，没有可以支配的个体了
    while (front[i] != []):
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if (n[q] == 0):
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i = i + 1
        front.append(Q)

    del front[len(front) - 1]  # 删除了最后一层无支配个体的front层,最后一层是空集
    return front


# Function to calculate crowding distance  同层之间的一个计算
def crowding_distance(values1, values2, front):
    # distance = [0 for i in range(len(front))]
    lenth = len(front)
    for i in range(lenth):
        distance = [0 for i in range(lenth)]
        sorted1 = sort_by_values(front, values1[:])  # 找到front中的个体索引序列
        sorted2 = sort_by_values(front, values2[:])  # 找到front中的个体索引序列
        distance[0] = 4444
        distance[lenth - 1] = 4444
        for k in range(2, lenth - 1):
            distance[k] = distance[k] + (values1[sorted1[k + 1]] - values1[sorted1[k - 1]]) / (
                        max(values1) - min(values1))
            # print("/n")
            print("k:", k)
            print("distance[{}]".format(k), distance[k])
        for k in range(2, lenth - 1):
            distance[k] = distance[k] + (values2[sorted2[k + 1]] - values2[sorted2[k - 1]]) / (
                        max(values2) - min(values2))
    return distance


# #Function to carry out the crossover
def crossover(a, b):
    r = random.random()
    if r > 0.5:
        return mutation((a + b) / 2)
    else:
        return mutation((a - b) / 2)


# #Function to carry out the mutation operator
def mutation(solution):
    mutation_prob = random.random()
    if mutation_prob < 1:
        solution = min_x + (max_x - min_x) * random.random()
    return solution


# Main program starts here
pop_size = 10
max_gen = 100

# Initialization
min_x = -55
max_x = 55
solution = [min_x + (max_x - min_x) * random.random() for i in range(0, pop_size)]
print('solution', solution)
gen_no = 0
while (gen_no < max_gen):
    print('\n')
    print('gen_no:迭代次数', gen_no)
    function1_values = [function1(solution[i]) for i in range(0, pop_size)]
    function2_values = [function2(solution[i]) for i in range(0, pop_size)]
    print('function1_values:', function1_values)
    print('function2_values:', function2_values)
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:])
    print('front', non_dominated_sorted_solution)
    # print("The best front for Generation number ",gen_no, " is")
    # for valuez in non_dominated_sorted_solution[0]:
    #     print("solution[valuez]",round(solution[valuez],3),end=" ")
    #     print("\n")
    crowding_distance_values = []
    for i in range(0, len(non_dominated_sorted_solution)):
        crowding_distance_values.append(
            crowding_distance(function1_values[:], function2_values[:], non_dominated_sorted_solution[i][:]))
    print("crowding_distance_values", crowding_distance_values)
    solution2 = solution[:]
    # Generating offsprings
    while (len(solution2) != 2 * pop_size):
        a1 = random.randint(0, pop_size - 1)
        b1 = random.randint(0, pop_size - 1)
        solution2.append(crossover(solution[a1], solution[b1]))
    print('solution2', solution2)
    function1_values2 = [function1(solution2[i]) for i in range(0, 2 * pop_size)]
    function2_values2 = [function2(solution2[i]) for i in range(0, 2 * pop_size)]
    non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:], function2_values2[:])  # 2*pop_size
    print('non_dominated_sorted_solution2', non_dominated_sorted_solution2)
    # print("\n")
    crowding_distance_values2 = []
    for i in range(0, len(non_dominated_sorted_solution2)):
        crowding_distance_values2.append(
            crowding_distance(function1_values2[:], function2_values2[:], non_dominated_sorted_solution2[i][:]))

    print('crowding_distance_values2', crowding_distance_values2)
    new_solution = []
    for i in range(0, len(non_dominated_sorted_solution2)):
        non_dominated_sorted_solution2_1 = [
            index_of(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in
            range(0, len(non_dominated_sorted_solution2[i]))]
        print('non_dominated_sorted_solution2_1:', non_dominated_sorted_solution2_1)
        front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
        print("front22", front22)
        front = [non_dominated_sorted_solution2[i][front22[j]] for j in
                 range(0, len(non_dominated_sorted_solution2[i]))]
        print('front', front)
        front.reverse()
        for value in front:
            new_solution.append(value)
            if (len(new_solution) == pop_size):
                break
        if (len(new_solution) == pop_size):
            break
    solution = [solution2[i] for i in new_solution]
    gen_no = gen_no + 1

# Lets plot the final front now
function1 = [i * -1 for i in function1_values]
function2 = [j * -1 for j in function2_values]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()