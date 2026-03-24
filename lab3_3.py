import random
number=random.randint(1,100)
print('I have a number in mind')
while True:
    guess=int(input('Enter your guess:'))
    if guess<number:
        print('Too small')
    elif guess>number:
        print('Too large')
    else:
        print('Well done!')
        break