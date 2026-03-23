class Animal:
    def __init__(self, name):
        self.Name = name
    def makeSound(self):
        print("{}发声".format(self.Name))
    def move(self, distance):
        print("{}走了{}米".format(self.Name, distance))
    def move2(self, distance):
        print("{}飞行了{}米".format(self.Name, distance))
    def layEgg(self):
        print("{}下了个蛋".format(self.Name))

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)
    def makeSound(self):
        super().makeSound()
        print("汪汪...汪...")

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name)
    def makeSound(self):
        super().makeSound()
        print("喵...喵...")

class Bird(Animal):
    def __init__(self, name):
        super().__init__(name)
    def makeSound(self):
        super().makeSound()
        print("吱吱...吱吱...")
    def layEgg(self):
        super().layEgg()

def main():
    an = Cat("小猫卡迪")
    an.makeSound()
    an.move(10)
    print("---------------")
    dg = Dog("小狗丹尼")
    dg.makeSound()
    dg.move(20)
    print("---------------")
    bd = Bird("鹦鹉波利")
    bd.makeSound()
    bd.move2(50)
    bd.layEgg()
main()