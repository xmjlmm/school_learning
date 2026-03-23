'''
def Travel(travel_dict, year, place):
    if year in travel_dict:
        travel_dict[year].append(place)
    else:
        travel_dict[year] = [place]
    return travel_dict

def main():
    travel_plans = {}
    while True:
        year = input("请输入计划旅游的年份，或输入'完成'以结束：")
        if year == "完成":
            break
        place = input("请输入计划旅游的地点：")
        travel_plans = Travel(travel_plans, year, place)
        print(travel_plans)
main()
'''

'''
def Tick(travel_dict, year, place):
    try:
        year = str(int(year))
        travel_dict[year].remove(place)
        return travel_dict
    except ValueError:
        print('输入月份的格式不正确')
    except TypeError:
        print("未找到在{}年的{}旅行计划。".format(year, place))
    except KeyError:
        print('输入的月份错误')
    finally:
        print('更改完成')

def main():
    travel_plans = {"2023": ["北京", "上海"], "2024": ["广州", "深圳"]}
    while True:
        year = input("请输入完成旅游的年份，或输入'完成'以结束：")
        if year == "完成":
            break
        place = input("请输入完成旅游的地点：")
        travel_plans = Tick(travel_plans, year, place)
        print(travel_plans)
main()
'''

'''
def last_remaining(n, m):
    if n < 1 or m < 1:
        return -1
    remaining = list(range(n))
    current = 0
    while len(remaining) > 1:
        current = (current + m - 1) % len(remaining)
        del remaining[current]
    return remaining[0]

def main():
    n = int(input('n='))
    m = int(input('m='))
    print(last_remaining(n, m))
main()
'''
'''
def Tick(travel_dict, year, place):
    try:
        year = str(int(year))
        travel_dict[year].remove(place)
        return travel_dict
    except ValueError:
        print('输入的年份应该是一个数字。')
    except KeyError:
        print('在旅行计划中没有找到{}年的记录。'.format(year))
    except TypeError:
        print("'NoneType' object is not subscriptable")
    finally:
        print('更改完成')

def main():
    travel_plans = {"2023": ["北京", "上海"], "2024": ["广州", "深圳"]}
    while True:
        year = input("请输入完成旅游的年份，或输入'完成'以结束：")
        if year == "完成":
            break
        place = input("请输入完成旅游的地点：")
        travel_plans = Tick(travel_plans, year, place)
        print(travel_plans)
main()
'''
'''
def Tick(travel_dict, year, place):
    try:
        year = str(int(year))
        if year in travel_dict:
            if place in travel_dict[year]:
                travel_dict[year].remove(place)
                if len(travel_dict[year]) == 0:
                    del travel_dict[year]
            else:
                print("在{0}年的旅行计划中没有找到地点{1}。".format(year,place))
        else:
            print('在旅行计划中没有找到{0}年的记录。'.format(year))
    except ValueError:
        print('输入的年份应该是一个数字。')
    except:
        print("出现了一个错误: ")
    finally:
        print('更改完成')
        return travel_dict
def main():
    travel_plans = {"2023": ["北京", "上海"], "2024": ["广州", "深圳"]}
    while True:
        year = input("请输入完成旅游的年份，或输入'完成'以结束：")
        if year == "完成":
            break
        place = input("请输入完成旅游的地点：")
        travel_plans = Tick(travel_plans, year, place)
        print(travel_plans)
main()'''

'''
import random
class Hero:
    def __init__(self, name, health, attack, defense,Criticalrate,Criticaldamage,team = None):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.Criticalrate = Criticalrate
        self.Criticaldamage = Criticaldamage
        self.team = None  # 初始时未加入任何队伍
    def join_team(self, other_hero):
        self.team = other_hero
        return (self.name,other_hero.name)
    def attack_enemy(self):
        if self.team is None:
            print("{0}没有队伍，无法组队".format(self.name))
            return
        enemy = self.team
        damage = self.attack
        while True:
            t = random.random()
            if t < self.Criticalrate:
                damage = round(damage * (self.Criticaldamage + 1) - enemy.defense,1)
            else:
                damage = damage - enemy.defense
            if damage < enemy.defense:
                print("{0}的攻击力太低，无法对{1}造成伤害".format(self.name,enemy.name))
                return
            enemy.health -= damage
            enemy.health = round(enemy.health,2)
            print("{0}对{1}造成了{2}点伤害,{3}剩余{4}血".format(self.name,enemy.name,damage,enemy.name,enemy.health))
# 创建两个英雄实例
h1 = Hero('白起',100,25,10,0.5,0.5,2.0)
h2 = Hero('程咬金',120,20,15,0.5,0.5,3.0)
# 组队
h1.join_team(h2)
h2.join_team(h1)
print('队伍：',h1.join_team(h2))
# 战斗
while h1.health > 0 and h2.health > 0:
    h1.attack_enemy()
    if h2.health <= 0:
        print("{0}获胜".format(h1.name))
        break
    h2.attack_enemy()
    if h1.health <= 0:
        print("{0}获胜".format(h2.name))
        break
'''

import random
class Hero:
    def __init__(self, name, health, attack, defense,Criticalrate,Criticaldamage,team = None):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.Criticalrate = Criticalrate
        self.Criticaldamage = Criticaldamage
        self.team = None  # 初始时未加入任何队伍
    def join_team(self, other_hero):
        self.team = other_hero
        return (self.name,other_hero.name)
    def attack_enemy(self,enemy):
        t = random.random()   #概率越大，表示越有可能暴击
        if t < self.Criticalrate:
            damage = round(self.attack * (self.Criticaldamage + 1) - enemy.defense,1)
        else:
            damage = self.attack - enemy.defense
        if damage < enemy.defense:
            print("{0}的攻击力太低，无法对{1}造成伤害".format(self.name,enemy.name))
            return
        enemy.health -= damage
        enemy.health = round(enemy.health,2)
        print("{0}对{1}造成了{2}点伤害,{3}剩余{4}血".format(self.name,enemy.name,damage,enemy.name,enemy.health))
# 创建两个英雄实例
h1 = Hero('白起',100,25,10,0.5,0.5,2.0)
h2 = Hero('程咬金',120,20,15,0.5,0.5,3.0)
# 组队
h1.join_team(h2)
h2.join_team(h1)
print('队伍：',h1.join_team(h2))
# 战斗
while h1.health > 0 and h2.health > 0:
    h1.attack_enemy(h2)
    if h2.health <= 0:
        print("{0}获胜".format(h1.name))
        break
    h2.attack_enemy(h1)
    if h1.health <= 0:
        print("{0}获胜".format(h2.name))
        break

'''
import random
class Upgrade(Hero):
    def __init__(self,name,health,attack,defense,Criticalrate,Criticaldamage,hero_type,team = None):
        Hero.__init__(self, name, health, attack, defense,Criticalrate,Criticaldamage,team = None)
        self.hero_type = hero_type
    def hero_team(self,second,third,forth):
        try:
            if self.hero_type != second.hero_type:
                return ((self.name, second.name), (third.name, forth.name))
            elif self.hero_type != third.hero_type:
                return ((self.name, third.name), (second.name, forth.name))
            elif self.hero_type != forth.hero_type:
                return ((self.name, forth.name), (second.name, third.name))
        except:
            print('物理和法师英雄不均衡')

    def can_battle(self):
        return random.random() < 0.5

    def calculate_damage(self):
        damage = random.randint(1, self.attack)
        if self.hero_type == "物理":
            return damage
        elif self.hero_type == "法术":
            return damage * 0.5

    def attack_enemy(self, enemy):
        print("{0}发起了攻击！".format(self.name))
        if enemy.hero_type != self.hero_type and random.random() < 0.2:
            print("对方免疫了伤害！")
        else:
            damage = self.calculate_damage()
            damage -= enemy.defense
            damage = max(damage, 0)
            enemy.health -= damage
            print("{0}受到了{1}点伤害！".format(enemy.name,damage))

# 创建两个不同类型的英雄实例
hero1 = Upgrade("元哥", 100, 50, 20, 0.5, 0.5, "物理")
hero2 = Upgrade("妲己", 100, 30, 10, 0.5, 0.5, "法术")
hero3 = Upgrade("木兰", 100, 50, 20, 0.5, 0.5, "物理")
hero4 = Upgrade("猫咪", 100, 30, 10, 0.5, 0.5, "法术")

# 组队
team = hero1.hero_team(hero2,hero3,hero4)
print(team)
team1 = team[0]
team2 = team[1]
t = random.random()
if t > 0.5:
    team1_canbattle = team[0][0]
    team2_canbattle = team[1][0]
else:
    team1_canbattle = team[0][1]
    team2_canbattle = team[1][1]
print(team1_canbattle)
print(team2_canbattle)
# 模拟战斗
rounds = 1
while hero1.health > 0 and hero2.health > 0:
    print("第{0}回合开始！".format(rounds))
    if hero1.can_battle():
        hero1.attack_enemy(hero2)
    else:
    if hero2.can_battle():
        hero2.attack_enemy(hero1)
    print("{0}剩余生命值：{1}".format(hero1.name, hero1.health))
    print("{0}剩余生命值：{1}".format(hero2.name, hero2.health))
    rounds += 1

if hero1.health <= 0:吗
    print(f"{hero2.name}获胜！")
else:
    print(f"{hero1.name}获胜！")
    '''
#导入所需要的模块
import random
#定义类
class Upgrade(Hero):
    def __init__(self,name,health,attack,defense,Criticalrate,Criticaldamage,hero_type,team = None):
        Hero.__init__(self, name, health, attack, defense,Criticalrate,Criticaldamage,team = None)
        self.hero_type = hero_type
    #定义组队函数
    def hero_team(self, second, third, forth):
        try:
            if self.hero_type != second.hero_type:
                return ((self.name, second.name), (third.name, forth.name))
            elif self.hero_type != third.hero_type:
                return ((self.name, third.name), (second.name, forth.name))
            elif self.hero_type != forth.hero_type:
                return ((self.name, forth.name), (second.name, third.name))
        except:
            print('物理和法师英雄不均衡')
        finally:
            print('end')
    #定义出战函数
    def can_battle(self):
        return random.random() < 0.5
    #定义免疫和进攻
    def attack_enemy(self, enemy):
        print("{0}发起了攻击！".format(self.name))
        damage = self.attack
        if self.hero_type != enemy.hero_type:
            print("由于进攻方和防守方的属性不同，因此对方获得了20%的伤害免疫！")
            t = random.random()
            if t < 0.2:
                damage = 0
        rat = random.random()   #概率越大，表示越有可能暴击
        if rat < self.Criticalrate:
            damage = round(self.attack * (self.Criticaldamage + 1) - enemy.defense,1)
        else:
            damage = self.attack - enemy.defense
        if damage < enemy.defense:
            print("{0}的攻击力太低，无法对{1}造成伤害".format(self.name,enemy.name))
            return
        enemy.health -= damage
        enemy.health = round(enemy.health,2)
        print("{0}对{1}造成了{2}点伤害,{3}剩余{4}血".format(self.name,enemy.name,damage,enemy.name,enemy.health))

# 创建两个不同类型的英雄实例
hero1 = Upgrade("元哥", 100, 50, 20, 0.5, 0.5, "物理")
hero2 = Upgrade("妲己", 100, 30, 10, 0.5, 0.5, "法术")
hero3 = Upgrade("木兰", 100, 50, 20, 0.5, 0.5, "物理")
hero4 = Upgrade("猫咪", 100, 30, 10, 0.5, 0.5, "法术")
# 组队
team = hero1.hero_team(hero2, hero3, hero4)
print(team)
team1 = team[0]
team2 = team[1]
# 模拟战斗
rounds = 1
while hero1.health > 0 and hero2.health > 0 and hero3.health > 0 and hero4.health > 0:
    print("第{0}回合开始！".format(rounds))
    if hero1.can_battle():
        if hero3.can_battle():
            hero1.attack_enemy(hero3)
            hero3.attack_enemy(hero1)
            print("{0}剩余生命值：{1}".format(hero1.name, hero1.health))
            print("{0}剩余生命值：{1}".format(hero3.name, hero3.health))
        else:
            hero1.attack_enemy(hero4)
            hero4.attack_enemy(hero1)
            print("{0}剩余生命值：{1}".format(hero1.name, hero1.health))
            print("{0}剩余生命值：{1}".format(hero4.name, hero4.health))
    else:
        if hero3.can_battle():
            hero2.attack_enemy(hero3)
            hero3.attack_enemy(hero2)
            print("{0}剩余生命值：{1}".format(hero2.name, hero2.health))
            print("{0}剩余生命值：{1}".format(hero3.name, hero3.health))
        else:
            hero2.attack_enemy(hero4)
            hero4.attack_enemy(hero2)
            print("{0}剩余生命值：{1}".format(hero2.name, hero2.health))
            print("{0}剩余生命值：{1}".format(hero4.name, hero4.health))
    rounds += 1
if hero1.health <= 0 or hero2.health <= 0:
    print("{0}获胜！".format(team1))
elif hero3.health <= 0 or hero4.health <= 0:
    print("{0}获胜！".format(team2))