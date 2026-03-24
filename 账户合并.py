class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        # # 假设说有一个字典，那么字典的键是名字，字典的值是邮箱列表
        # length, d = len(accounts), {}
        # for i in range(length):
        #     cur_ele = accounts[i]
        #     name = cur_ele[0]
        #     email = cur_ele[1:]
        #     if name not in d:
        #         d[name] = email
        #     else:



        length, ans = len(accounts), []
        if
            return ans
        name = accounts[0][0]
        accounts[0] = list(set(accounts[0][1:]))
        accounts[0].sort()
        accounts[0].insert(0, name)
        ans.append(accounts[0])
        for i in range(1, length, 1):
            name, flag = accounts[i][0], 0
            for j in range(0, len(ans), 1):
                if name == ans[j][0]:
                    for k in range(1, len(accounts[i]), 1):
                        if accounts[i][k] in ans[j]:
                            tmp = (list(set(ans[j][1:] + accounts[i][1:])))
                            tmp.sort()
                            tmp.insert(0, name)
                            ans.append(tmp)
                            del ans[j]
                            flag = 1
                            break
            if flag == 0:
                name = accounts[i][0]
                accounts[i] = list(set(accounts[i][1:]))
                accounts[i].sort()
                accounts[i].insert(0, name)
                ans.append(accounts[i])
        return self.accountsMerge(ans)

        # length, real_ans = len(ans), []
        # name = ans[0][0]
        # ans[0] = list(set(ans[0][1:]))
        # ans[0].sort()
        # ans[0].insert(0, name)
        # real_ans.append(ans[0])
        # for i in range(1, length, 1):
        #     name, flag = ans[i][0], 0
        #     for j in range(0, len(real_ans), 1):
        #         if name == real_ans[j][0]:
        #             for k in range(1, len(ans[i]), 1):
        #                 if ans[i][k] in ans[j]:
        #                     tmp = (list(set(real_ans[j][1:] + ans[i][1:])))
        #                     tmp.sort()
        #                     tmp.insert(0, name)
        #                     real_ans.append(tmp)
        #                     del real_ans[j]
        #                     flag = 1
        #                     break
        #     if flag == 0:
        #         name = ans[i][0]
        #         ans[i] = list(set(ans[i][1:]))
        #         ans[i].sort()
        #         ans[i].insert(0, name)
        #         real_ans.append(ans[i])
        #
        # return real_ans

def main():
    s = Solution()
    accounts = [["David","David0@m.co","David1@m.co"],["David","David3@m.co","David4@m.co"],["David","David4@m.co","David5@m.co"],["David","David2@m.co","David3@m.co"],["David","David1@m.co","David2@m.co"]]
    print(s.accountsMerge(accounts))

if __name__ == '__main__':
    main()