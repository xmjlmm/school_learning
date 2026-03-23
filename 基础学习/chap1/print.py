'''


#可以输出数字
print(520)
print(98)

#可以输出字符串
print('helloworld')
print("helloworld")

#含有运算符的表达式
print(1+3)

#将数据输出文件中   ,注意点,1,所指定的盘符存在 ， 2，使用file=fp
fp=open('D:/text.txt','a+') #a+如果文件不存在就创建，存在就在文件内容的后面继续追加
print('helloworld',file=fp)
fp.close()

#不进行换行输出（输出内容在一行当中）
print('hello','world','python')

'''


import random
class Hero:
    def __init__(self, name, health, attack, defense,Criticalrate,Criticaldamage,Speedattack,team = None):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.Criticalrate = Criticalrate
        self.Criticaldamage = Criticaldamage
        self.Speedattack = Speedattack
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
                damage = damage * (self.Criticaldamage + 1) - enemy.defense
            else:
                damage = damage - enemy.defense
            if self.attack < enemy.defense:
                print("{0}的攻击力太低，无法对{1}造成伤害".format(self.name,enemy.defense))
                return
            enemy.health -= damage
            print("{0}对{1}造成了{2}点伤害,{3}剩余{4}血".format(self.name,enemy.name,damage,enemy.name,enemy.health))

# 创建两个英雄实例
h1 = Hero('白起',100,20,10,0.5,0.5,2.0)
h2 = Hero('程咬金',120,15,15,0.4,0.6,3.0)

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
