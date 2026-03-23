#
#
# def calculate_order_price(coffee_type, quantity, price_dict):
#     total_price = price_dict[coffee_type] * quantity
#     return total_price
#
# def main():
#     # 定义咖啡的价格字典
#     price_dict = {
#         "美式咖啡": 5.0,
#         "拿铁咖啡": 7.0,
#         "卡布奇诺": 6.0
#     }
#
#     # 订单列表，每个订单是一个包含顾客姓名、咖啡种类和数量的元组
#     orders = [
#         ("张三", "美式咖啡", 2),
#         ("李四", "拿铁咖啡", 1),
#         ("王五", "卡布奇诺", 1)
#     ]
#
#     # 输出每个订单的详细信息，包括顾客姓名、咖啡种类和数量，以及总价
#     for order in orders:
#         customer_name, coffee_type, quantity = order
#         total_price = calculate_order_price(coffee_type, quantity, price_dict)
#         print(f"顾客姓名: {customer_name}, 咖啡种类: {coffee_type}, 数量: {quantity}, 总价: {total_price}")
#
# if __name__ == "__main__":
#     main()


# def calculate_order_total(coffees, quantities, price_dict):
#     # 初始化订单总价为0
#     total = 0
#
#     # 确保咖啡种类和数量的列表长度相同
#     if len(coffees) != len(quantities):
#         raise ValueError("The lengths of coffees and quantities lists must be the same.")
#
#         # 遍历每种咖啡和对应的数量
#     for coffee, quantity in zip(coffees, quantities):
#         # 检查咖啡是否在价格字典中
#         if coffee not in price_dict:
#             raise KeyError(f"Unknown coffee type: {coffee}")
#
#             # 计算当前咖啡的总价，并累加到订单总价
#         total += price_dict[coffee] * quantity
#
#         # 返回订单总价
#     return total
#
#
# # 示例价格字典
# price_dict = {
#     'latte': 3.5,
#     'cappuccino': 4.0,
#     'espresso': 2.0,
#     'mocha': 4.5
# }
#
# # 示例订单
# coffees = ['latte', 'cappuccino', 'latte']
# quantities = [2, 1, 1]
#
# # 计算订单总价
# total_price = calculate_order_total(coffees, quantities, price_dict)
# # print(f"The total price of the order is: {total_price}")


# for i in range(2,2):
#     print('1')