n = int(input())
# first_ASCll = 97
cruises = []
prices = []
for _ in range(n):
    list_price = input()
    cruise = list_price.split(' ')[0]
    price = list_price.split(' ')[1]
    cruises.append(cruise)
    prices.append(int(price))
cruise_orders = input()
cruise_cout = []
sum_price = 0
for cruise in cruise_orders:
    index = cruises.index(cruise)
    price = prices[index]
    if cruise not in cruise_cout:
        cruise_cout.append(cruise)
        sum_price = sum_price + price
    else:
        sum_price = sum_price + price // 2

print(sum_price)