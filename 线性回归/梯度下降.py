'''
# 创建一个空字典来存储学生成绩
student_scores = {}
# 主程序循环
while True:
    print('学生成绩管理系统')
    print('#1.添加成绩')
    print('#2.删除成绩')
    print('#3.查看成绩')
    choice = input('请选择操作 (1/2/3) 或输入 end 结束: ')
    if choice == '1':
        # 添加成绩
        student_id = input('请输入学号: ')
        score = input('请输入分数: ')
        # 检查学号是否已存在
        if student_id in student_scores:
            print('该学号已存在，不允许重复添加成绩。')
        else:
            student_scores[student_id] = score
            print('成绩已添加。')
    elif choice == '2':
        # 删除成绩
        student_id = input('请输入要删除成绩的学号: ')
        if student_id in student_scores:
            del student_scores[student_id]
            print('成绩已删除。')
        else:
            print('未找到该学号的成绩。')
    elif choice == '3':
        # 查看成绩
        student_id = input('请输入要查看成绩的学号: ')
        if student_id in student_scores:
            print('学号:{}, 成绩:{}'.format(student_id,student_score[student_id]))
        else:
            print('未找到该学号的成绩。')
    elif choice == 'end':
        break
    else:
        print('无效的选择，请重新输入。')
print('程序结束。')
'''
'''
import math
def most(volunteer):
    length = len(volunteer)
    max = 0
    for i in range(length):
        volunteer_i = volunteer[i]
        event_i = len(volunteer_i) - 1
        if event_i > max:
            max = event_i
        else:
            continue
    return max
def special(volunteer):
    length = len(volunteer)
    d = {}
    for i in range(length):
        volunteer_i = volunteer[i]
        event_i = len(volunteer_i)
        for e in range(1,event_i):
            if volunteer_i[e] not in d:
                d[volunteer_i[e]] = volunteer_i[0]
            else:
                d[volunteer_i[e]] += volunteer_i[0]
    special = []
    for key in d:
        if len(d[key]) == 2:
            special.append((key,d[key]))
    return special
def main():
    volunteer = (('01','CET6','摄影','写作'), ('02','CET4'),
                 ('03','写作','手绘'), ('04','摄影','小语种','有其他志愿服务经验'),
                 ('05','CET6','剪辑','摄影'), ('06','有其他志愿服务经验'),
                 ('07','CET4'), ('08','写作'),
                 ('09','CET6','小语种','手语'), ('10','手绘','CET4'))
    print(most(volunteer))
    print(special(volunteer))
main()
'''
'''
def most_listened_artists_by_year(music):
    year_to_artist = {}
    for entry in music:
        year_month, artist = entry
        year = year_month.split('-')[0]
        if year not in year_to_artist:
            year_to_artist[year] = []
        year_to_artist[year].append(artist)
    for year, artists in year_to_artist.items():
        artist_count = {}
        for artist in artists:
            if artist in artist_count:
                artist_count[artist] += 1
            else:
                artist_count[artist] = 1
        most_listened_artist = max(artist_count, key=artist_count.get)
        print(f"在{year}年，最常听的歌手是：{most_listened_artist}")
music = (('2022-01', 'Taylor Swift'), ('2022-06', '五月天'),
 ('2023-01', '五月天'), ('2022-02', 'Taylor Swift'),
 ('2023-03', 'Ed Sheeran'), ('2023-03', 'Ed Sheeran'),
 ('2023-10', 'Taylor Swift'), ('2022-01', 'Taylor Swift'),
 ('2022-10', 'Ed Sheeran'), ('2023-03', '五月天'),
 ('2022-06', 'Ed Sheeran'), ('2023-01', 'Ed Sheeran'),
 ('2021-03', '五月天'), ('2022-03', 'Taylor Swift'),
 ('2021-05', '五月天'), ('2022-12', '五月天'),
 ('2022-12', '五月天'), ('2022-06', 'Ed Sheeran'),
 ('2023-06', 'Ed Sheeran'), ('2021-02', 'Taylor Swift'))
most_listened_artists_by_year(music)
'''
'''
def most_listened_artists_by_year(music):
    length = len(music)
    years = [2021,2022,2023]
    ls = []
    for year in years:
        d = {}
        for i in range(length):
            if music[i][0][0:4] == year:
                if music[i][1] not in d:
                    d[music[i][1]] = 0
                else:
                    d[music[i][1]] += 1
        ls.append(d)
    return ls
def main():
    music = (('2022-01', 'Taylor Swift'), ('2022-06', '五月天'),
        ('2023-01', '五月天'), ('2022-02', 'Taylor Swift'),
        ('2023-03', 'Ed Sheeran'), ('2023-03', 'Ed Sheeran'),
        ('2023-10', 'Taylor Swift'), ('2022-01', 'Taylor Swift'),
        ('2022-10', 'Ed Sheeran'), ('2023-03', '五月天'),
        ('2022-06', 'Ed Sheeran'), ('2023-01', 'Ed Sheeran'),
        ('2021-03', '五月天'), ('2022-03', 'Taylor Swift'),
        ('2021-05', '五月天'), ('2022-12', '五月天'),
        ('2022-12', '五月天'), ('2022-06', 'Ed Sheeran'),
        ('2023-06', 'Ed Sheeran'), ('2021-02', 'Taylor Swift'))
    print(most_listened_artists_by_year(music))
main()
'''
'''
def most_listened_artists_by_year(music):
    years = [2021, 2022, 2023]
    ls = []
    for year in years:
        d = {}
        for item in music:
            if int(item[0][0:4]) == year:
                if item[1] not in d:
                    d[item[1]] = 1
                else:
                    d[item[1]] += 1
        ls.append(d)

    length_ls = len(ls)
    ls_most = []
    for i in range(length_ls):
        dict = ls[i]
        ls_year = sorted(dict.items(),key = lambda x:x[1],reverse = False)
        ls_most.append((str(i + 2021),ls_year[0][0],ls_year[0][1]))
    return ls_most

def main():
    music = [
        ('2022-01', 'Taylor Swift'), ('2022-06', '五月天'),
        ('2023-01', '五月天'), ('2022-02', 'Taylor Swift'),
        ('2023-03', 'Ed Sheeran'), ('2023-03', 'Ed Sheeran'),
        ('2023-10', 'Taylor Swift'), ('2022-01', 'Taylor Swift'),
        ('2022-10', 'Ed Sheeran'), ('2023-03', '五月天'),
        ('2022-06', 'Ed Sheeran'), ('2023-01', 'Ed Sheeran'),
        ('2021-03', '五月天'), ('2022-03', 'Taylor Swift'),
        ('2021-05', '五月天'), ('2022-12', '五月天'),
        ('2022-12', '五月天'), ('2022-06', 'Ed Sheeran'),
        ('2023-06', 'Ed Sheeran'), ('2021-02', 'Taylor Swift')
    ]
    print(most_listened_artists_by_year(music))
main()
''''''
satisfaction = [-1,-8,0,5,-7]
length = len(satisfaction)
plus = []
minus = []
while length > 0:
    if not satisfaction:
        break
    ele = satisfaction.pop()
    if ele >= 0:
        plus.append(ele)
    else:
        minus.append(ele)
    plus.sort()
    minus.sort()
    sum = 0
    for i in range(len(plus)):
        sum = sum + plus[i] * (i + 1)
    le = len(minus)
    while le > 0:
        if not minus:
            break
        t = minus.pop()
        plus.append(t)
        plus.sort()
        sum_i = 0
        for i in range(len(plus)):
            sum = sum + plus[i] * (i + 1)
        if sum_i > sum:
            sum = sum_i
print(sum)
'''
import math
n = 5
mp = [[math.inf] * n for _ in range(n)]
print(mp)
mp[0][1] = 2
print(mp)
ls = [[math.inf] * n ] * n
print(ls)
ls[0][1] = 2
print(ls)