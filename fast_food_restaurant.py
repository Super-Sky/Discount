"""
- 该店的菜品每一个都有一个唯一的id
- 当前的优惠方式有:
  - 满30减6元
  - 指定菜品半价
- 除菜品外没有其它收费（如送餐费、餐盒费等）
- 如果两种优惠方式省钱一样多，则使用前一种优惠方式
"""

from abc import ABC, abstractmethod


class Promotion(ABC):

    def __init__(self):
        self.food_price_map = {
            "ITEM0001":18,
            "ITEM0013":6,
            "ITEM0022":8,
        }
        self.satisfy_money = 30
        self.reduce_money = 6
        self.discount_food = ["ITEM0001","ITEM0022"]
        self.discount_number = 0.5

    @abstractmethod
    def discount(self, order_dict):
        pass


class OriginalPromotion(Promotion):
    def discount(self,order_dict):
        price_all = 0
        for food in order_dict.keys():
            price_all += self.food_price_map[food]*order_dict[food]
        return {"Original":price_all}


class ReducePromotion(Promotion):
    def discount(self, order_dict):
        price_all = 0
        for food in order_dict.keys():
            price_all += self.food_price_map[food]*order_dict[food]
        if price_all >=self.satisfy_money:
            price_all -= self.reduce_money
        return {"Reduce":price_all}


class DiscountPromotion(Promotion):
    def discount(self, order_dict):
        price_all = 0
        for food in order_dict.keys():
            if food in self.discount_food:
                price_all += self.food_price_map[food]*order_dict[food]*self.discount_number
            else:
                price_all += self.food_price_map[food]*order_dict[food]
        return {"Discount":price_all}

class Order(object):

    discount_map = {
        "Original": OriginalPromotion,
        "Reduce": ReducePromotion,
        "Discount": DiscountPromotion
    }

    def __init__(self, order_dict, coupon):
        self.order_dict = order_dict
        self.coupon = coupon

    def total_money(self):
        return self.discount_map.get(self.coupon)().discount(self.order_dict)

class Utils(object):

    def __init__(self):
        self.split_sign = "x"
        self.food_price_map = {
            "ITEM0001":18,
            "ITEM0013":6,
            "ITEM0022":8,
        }
        self.food_name_map = {
            "ITEM0001":"黄焖鸡",
            "ITEM0013":"肉夹馍",
            "ITEM0022":"凉皮",
        }
        self.discount_food_list = ["ITEM0001","ITEM0022"]

    def list_split_dict(self,datalist):
        data_split_dict = dict()
        for datastr in datalist:
            tempdatastrlist = datastr.split(self.split_sign)
            order = tempdatastrlist[0].strip()
            number = tempdatastrlist[1].strip()
            data_split_dict[order] = int(number)
        return data_split_dict

    def price_printing(self,food_number_dict):
        for food in food_number_dict.keys():
            number = food_number_dict[food]
            price = self.food_price_map[food]
            price_all = number*price
            foodname = self.food_name_map[food]
            # 黄焖鸡 x 1 = 18元
            print("{foodname} x {number} = {price_all}元".format(foodname=foodname,number=number,price_all=price_all))

    def discount_printing(self,nodepricedict,original_price,nodeprice,order_dict):
        foodlist = order_dict.keys()
        model = list(nodepricedict.keys())[0]
        if model == "Original":
            return
        print("使用优惠:")
        if model == "Reduce":
            #满30减6元，省6元
            print("满30减6元，省6元")
        elif model == "Discount":
            #指定菜品半价(黄焖鸡，凉皮)，省13元
            foods = ",".join([self.food_name_map[_] for _ in foodlist if _ in self.discount_food_list])
            reduce_money = original_price-nodeprice
            print("指定菜品半价({foods})，省{reduce_money}元".format(foods=foods,reduce_money=reduce_money))
        print("-----------------------------------")

    def total_printing(self,nodeprice):
        #总计：25元
        print("总计：{nodeprice}元".format(nodeprice=int(nodeprice)))
        print("===================================")


DiscountCategory = ["Reduce","Discount"]
Original = "Original"
# InitData = {
#     'ITEM0001': {
#         'id': 'ITEM0001',
#         'name': '黄焖鸡',
#         'price': 18.0,
#         'is_half_price': True  # 是否半价
#     },
#     'ITEM0013': {
#         'id': 'ITEM0013',
#         'name': '肉夹馍',
#         'price': 6.0,
#         'is_half_price': False  # 是否半价
#     },
#     'ITEM0022': {
#         'id': 'ITEM0022',
#         'name': '凉皮',
#         'price': 8.0,
#         'is_half_price': True  # 是否半价
#     }
# }

def bestCharge(order_list):
    u = Utils()
    order_dict = u.list_split_dict(order_list)
    print("============= 订餐明细 =============")
    u.price_printing(order_dict)
    print("-----------------------------------")
    original_price_dict = Order(order_dict, Original).total_money()
    nodepricedict = original_price_dict
    original_price = original_price_dict[Original]
    nodeprice = original_price_dict[Original]
    for Discount in DiscountCategory:
        nowpricedict =Order(order_dict, Discount).total_money()
        nowprice = nowpricedict[Discount]
        if nowprice < nodeprice:
            nodepricedict = nowpricedict
            nodeprice = nowprice
    u.discount_printing(nodepricedict,original_price,nodeprice,order_dict)
    u.total_printing(nodeprice)


if __name__ == '__main__':
    # order_list = ["ITEM0001 x 1", "ITEM0013 x 2", "ITEM0022 x 1"]
    # order_list = ["ITEM0013 x 4", "ITEM0022 x 1"]
    order_list = ["ITEM0013 x 4"]
    bestCharge(order_list)
