class Solution:
    def detectCapitalUse(self, word: str) -> bool:
        str_big = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        count_big_word = 0
        length = len(word)
        for alf in word:
            if alf in str_big:
                count_big_word += 1
        if count_big_word == length:
            return True
        if count_big_word == 0:
            return True
        if count_big_word == 1 and word[0] in str_big:
            return True
        return False

def main():
    s = Solution()
    print(s.detectCapitalUse('g'))

if __name__ == "__main__":
    main()