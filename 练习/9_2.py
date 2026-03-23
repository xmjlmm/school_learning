import random
def countLetter(chars):
    print("随机生成52个字母：")
    for i in range (52):
        x=chr(random.randint(ord('a'),ord('z')))
        chars.append(x)
    #print(chars)
    for i in range(52):
        print(chars[i],end=" ")

def counts(chars2):
    for i in range(97,123):
        x=chr(i)
        chars2.append(x)
    #print(chars2)

def printList(a,b):
    print("\n字母出现的次数：")
    freq=[]
    for i in range(26):
        freq.append(0)
    for i in range(0,52):
        for j in range(0,26):
            if(ord(a[i])-97==j):
                freq[j]+=1
    for i in range(0,26):
        print(b[i],end=" ")
    print()
    for i in range(0,26):
        print(freq[i],end=" ")

def main():
    a=[]
    b=[]
    countLetter(a)
    counts(b)
    printList(a,b)
main()