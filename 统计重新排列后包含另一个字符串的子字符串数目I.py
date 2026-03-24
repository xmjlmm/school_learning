class Solution:
    def validSubstringCount(self, word1: str, word2: str) -> int:
        target_length, compare_length = len(word1), len(word2)
        if target_length < compare_length:
            return 0

        d, ans = {}, 0
        for word in word2:
            if word not in d:
                d[word] = 1
            else:
                d[word] = d[word] + 1

        for i in range(compare_length, target_length+1):
            for j in range(0, target_length-i+1):
                cur, flag = word1[j:j+i:1], 0
                for word in d:
                    if cur.count(word) < d[word]:
                        flag = 1
                        break
                if flag == 0: 
                    ans = ans + 1
        return ans

def main():
    s = Solution()
    word1 = "abcabc"
    word2 = "abc"
    print(s.validSubstringCount(word1, word2))

if __name__ == '__main__':
    main()









# class Solution:
#     def validSubstringCount(self, word1: str, word2: str) -> int:
#         target_length, compare_length = len(word1), len(word2)
#         if target_length < compare_length:
#             return 0

#         d, ans = {}, 0
#         for word in word2:
#             if word not in d:
#                 d[word] = 1
#             else:
#                 d[word] = d[word] + 1

#         for i in range(compare_length, target_length+1):
#             for j in range(0, target_length-i+1):
#                 cur, flag = word1[j:j+i:1], 0
#                 for word in d:
#                     if cur.count(word) < d[word]:
#                         flag = 1
#                         break
#                 if flag == 0: 
#                     ans = ans + 1
#         return ans

# def main():
#     s = Solution()
#     word1 = "abcabc"
#     word2 = "abc"
#     print(s.validSubstringCount(word1, word2))

# if __name__ == '__main__':
#     main()