'''class Solution:
    def discountPrices(self, sentence: str, discount: int) -> str:
        ls = sentence.split(' ')
        length = len(ls)
        restrict = 'qwertyuiopasdfghjklzxcvbnm$'
        ans = ''
        for word in ls:
            count = 0
            for ci in word:
                if ci in restrict:
                    count += 1
            if count == 1 and word[0] == '$':
                price = word[1:]
                # 抽象的异常值处理, 一个个调试的时候才发现,淦
                if price == '':
                    ans = ans + '$ '
                    continue
                if '.' in price:
                    zheng, yu = price.split('.')
                    real_price = int(zheng) + int(yu) / (10 ** (len(yu)))
                else:
                    real_price = int(price)
                dis_price = real_price * (1 - discount / 100)
                result = '$' + '{:.2f}'.format(dis_price)
                ans = ans + result + ' '
            else:
                ans = ans + word + ' '
        return ans[0:-1:1]

def main():
    s = Solution()
    sentence = input('请输入一段话:')
    discount = int(input('请输入折扣:'))
    print(s.discountPrices(sentence, discount))

if __name__ == '__main__':
    main()
'''


class Solution:
    def discountPrices(self, sentence: str, discount: int) -> str:
        words = sentence.split()
        for i, word in enumerate(words):
            if word[0] == "$" and word[1:].isnumeric():
                price = int(word[1:]) * (1 - discount / 100)
                words[i] = f"${price:.2f}"
        return " ".join(words)

def main():
    s = Solution()
    sentence = input('请输入一段话:')
    discount = int(input('请输入折扣:'))
    print(s.discountPrices(sentence, discount))

if __name__ == '__main__':
    main()