import matplotlib.pyplot as plt
import random

def evaluate_guess(solution, guess):
    result = ''
    for s, g in zip(solution, guess):
        if s == g:
            result += 'Y'  # 字母正确，位置也正确
        elif g in solution:
            result += 'M'  # 字母正确，位置不正确
        else:
            result += 'N'  # 字母不在答案中
    return result

def simulate(wordle_solution):
    D_w = ['tools', 'brook', 'stool', 'shoot', 'loops']  # 示例词汇
    L_g = []
    for i in range(6):
        guess_word = random.choice(D_w)
        S_i = evaluate_guess(wordle_solution, guess_word)
        L_g.append(S_i)
        if S_i == 'YYYYY':
            break
        for j in range(5):
            if S_i[j] == 'Y':
                D_w = [w for w in D_w if w[j] == guess_word[j]]
            elif S_i[j] == 'M':
                D_w = [w for w in D_w if guess_word[j] in w and w[j] != guess_word[j]]
            elif S_i[j] == 'N':
                D_w = [w for w in D_w if guess_word[j] not in w]
    return L_g

# 修改simulate函数，只返回所需的答题次数
def simulate_attempts(wordle_solution):
    D_w = ['tools', 'brook', 'stool', 'shoot', 'loops']  # 示例词汇
    for i in range(6):
        guess_word = random.choice(D_w)
        S_i = evaluate_guess(wordle_solution, guess_word)
        if S_i == 'YYYYY':
            return i + 1  # 返回答题次数
        for j in range(5):
            if S_i[j] == 'Y':
                D_w = [w for w in D_w if w[j] == guess_word[j]]
            elif S_i[j] == 'M':
                D_w = [w for w in D_w if guess_word[j] in w and w[j] != guess_word[j]]
            elif S_i[j] == 'N':
                D_w = [w for w in D_w if guess_word[j] not in w]
    return 6  # 如果没有在6次内猜出，返回6

# 进行5000次模拟，并记录每次模拟的答题次数
attempts_distribution = [simulate_attempts('tools') for _ in range(5000)]

# 计算不同答题次数的概率
attempts_probs = {7-i: attempts_distribution.count(i) / 5000 for i in set(attempts_distribution)}

# 绘制答题次数的概率分布图
plt.bar(attempts_probs.keys(), attempts_probs.values(), color='skyblue')
plt.xlabel('Number of Attempts')
plt.ylabel('Probability')
plt.title('Probability Distribution of Number of Attempts')
plt.xticks(range(1, 7))
plt.show()

# 返回概率分布
attempts_probs
