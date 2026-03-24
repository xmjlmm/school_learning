import xalpha as xa
zzyl = xa.fundinfo('021580')
print(zzyl)
print(zzyl.info())
'''
华夏人工智能ETF联接D
fund name: 华夏人工智能ETF联接D
fund code: 021580
// 申购费
fund purchase fee: 0.0%
// 赎回费
fund redemption fee info: ['小于7天', '1.50%', '大于等于7天', '0.00%']
None'''


# 筛选出其 price数据里​​日期早于或等于2025年10月27日​​的所有记录，并将结果打印出来。
# print(zzyl.price[zzyl.price['date']<='2025-10-06'])
print(zzyl.price[(zzyl.price['date'] >= '2025-6-30') & (zzyl.price['date'] <= '2025-11-06')].to_string())
