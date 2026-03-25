import random
class Gift:
    """
    抽检类
    """
    def __init__(self, user_count):
        self.user_count = user_count

    @staticmethod
    def get_luck_body(start, end, count=2):
        if start == end:
            return [start]
        luck_list = []
        while len(luck_list) < count:
            luck = random.randint(start, end)
            if luck not in luck_list:
                luck_list.append(luck)
        return luck_list

    def prize_draw(self):
        """
        抽奖函数
        """

        if self.user_count < 100:
            print("抽奖人数不足100人")
            return

        section_list = [[11, 20], [21, 50]]
        for section in section_list:
            section_start, section_end = section
            section_end = min(section_end, self.user_count)
            luck_body = self.get_luck_body(section_start, section_end)
            print(
                "第{section_start}∼{section_end}名，每个区间，赛后直播随机抽取2名，每人¥30，中奖名单为：{luck_body}".format(
                    section_end=section_end, section_start=section_start, luck_body=luck_body))
            if section_end == self.user_count:
                break

        pre_section = [51, 100]
        n = 1
        while True:

            section_start = 100 * pow(2, n - 1) + 1
            section_end = min(100 * pow(2, n), self.user_count)
            # 如果这个周期不是满，就用这个周期的人数加上上个周期的人数去抽奖 结束循环
            if section_end < 100 * pow(2, n):
                section_start = pre_section[0]
                luck_body = self.get_luck_body(section_start, section_end, count=2)
                print(
                    "第{section_start}∼{section_end}名，每个区间，赛后直播随机抽取2名，每人¥30，中奖名单为：{luck_body}".format(
                        section_end=section_end, section_start=section_start, luck_body=luck_body))
                break
            # 如果这个周期是满的 则继续循环
            else:
                pre_section_start, pre_section_end = pre_section
                luck_body = self.get_luck_body(pre_section_start, pre_section_end, count=2)
                print(
                    "第{section_start}∼{section_end}名，每个区间，赛后直播随机抽取2名，每人¥30，中奖名单为：{luck_body}".format(
                        section_end=pre_section_end, section_start=pre_section_start, luck_body=luck_body))
                pre_section = [section_start, section_end]

            n += 1


if __name__ == '__main__':
    user_count = input()
    gift = Gift(int(user_count))
    gift.prize_draw()
