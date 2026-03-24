# 法2 首尾比较

class Solution:
    def validPalindrome(self, s: str) -> bool:
        left, right = 0, len(s)-1
        if right <= 1:
            return True
        flag = 0
        switch = 1
        while left < right and flag <= 1:
            if s[left] == s[right]:
                left += 1
                right -= 1
            else:
                flag += 1
                tmp_left, tmp_right = left, right
                if s[right-1] == s[left] and switch == 1:

                    right -= 2
                    left += 1

                # print(s[left], s[right])
                if s[left+1] == s[right] and switch == 2:
                    left += 2
                    right -= 1
                    print(left, right)
            if flag > 1:
                left, right = tmp_left, tmp_right
                flag = 0
                switch = switch + 1
            
            if switch > 2:
                break


            print(flag)
        if flag <= 1:
            return True
        return False
        
def main():
    s = Solution()
    word = "abc"
    print(s.validPalindrome(word))

if __name__ == "__main__":
    main()