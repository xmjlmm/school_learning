import pandas as pd
df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\预期销售量.xlsx", sheet_name= "Sheet2")
# 原始数据
data = {
    '作物名称':df['作物名称'],
    '单季': df['单季'],
    '第一季': df['第一季'],
    '第二季': df['第二季']
}

# 排序顺序
order = ['黄豆', '黑豆', '红豆', '绿豆', '爬豆', '小麦', '玉米', '谷子', '高粱', '黍子', '荞麦', '南瓜', '红薯', '莜麦', '大麦', '水稻', '豇豆', '刀豆', '芸豆', '土豆', '西红柿', '茄子', '菠菜', '青椒', '菜花', '包菜', '油麦菜', '小青菜', '黄瓜', '生菜', '辣椒', '空心菜', '黄心菜', '芹菜', '大白菜', '白萝卜', '红萝卜', '榆黄菇', '香菇', '白灵菇', '羊肚菌']

# 创建 DataFrame
df = pd.DataFrame(data)

# 按照给定的排序顺序重新排列
df['sort_order'] = df['作物名称'].apply(lambda x: order.index(x) if x in order else len(order))
df_sorted = df.sort_values('sort_order').drop(columns=['sort_order']).reset_index(drop=True)

print(df_sorted)
df_sorted.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\预期销售量(已排序).xlsx", sheet_name="Sheet2")