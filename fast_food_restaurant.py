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
        u = Utils()
        self.food_price_map = u.initdata_to_food_price_map()
        self.satisfy_money = InitData['config']['satisfy_money']
        self.reduce_money = InitData['config']['reduce_money']
        self.discount_food = InitData['config']['discount_food']
        self.discount_number =InitData['config']['discount_number']

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
        self.foods = 'foods'
        self.split_sign = InitData['config']['sign']
        self.satisfy_money = InitData['config']['satisfy_money']
        self.reduce_money = InitData['config']['reduce_money']
        self.food_price_map = self.initdata_to_food_price_map()
        self.food_name_map = self.initdata_to_food_name_map()
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
            print("满{satisfy_money}减{reduce_money}元，省{reduce_money}元".format(satisfy_money=self.satisfy_money,
                                                                             reduce_money=self.reduce_money))
        elif model == "Discount":
            #指定菜品半价(黄焖鸡，凉皮)，省13元
            foods = ",".join([self.food_name_map[_] for _ in foodlist if _ in self.discount_food_list])
            reduce_money = original_price-nodeprice
            print("指定菜品半价({foods})，省{reduce_money}元".format(foods=foods,reduce_money=int(reduce_money)))
        print("-----------------------------------")

    def total_printing(self,nodeprice):
        #总计：25元
        print("总计：{nodeprice}元".format(nodeprice=int(nodeprice)))
        print("===================================")

    def initdata_to_food_price_map(self):
        foodslist = InitData[self.foods]
        food_price_map = dict()
        for food_details in foodslist:
            food_price_map[food_details['id']] = food_details['price']
        return food_price_map

    def initdata_to_food_name_map(self):
        foodslist = InitData[self.foods]
        food_name_map = dict()
        for food_details in foodslist:
            food_name_map[food_details['id']] = food_details['name']
        return food_name_map

    def initdata_to_discount_food_list(self):
        foodslist = InitData[self.foods]
        discount_food_list = list()
        for food_details in foodslist:
            if food_details['is_half_price']:
                discount_food_list.append(food_details['id'])
        return discount_food_list


DiscountCategory = ["Reduce","Discount"]
Original = "Original"
InitData = {
    'config':{
        'sign':'x',
        'satisfy_money':30,
        'reduce_money':6,
        'discount_food':["ITEM0001","ITEM0022"],
        'discount_number':0.5
    },
    'foods':[
        {
            'id':'ITEM0001',
            'name': '黄焖鸡',
            'price': 18,
            'is_half_price': True  # 是否半价
        },
        {
            'id':'ITEM0013',
            'name': '肉夹馍',
            'price': 6,
            'is_half_price': False  # 是否半价
        },
        {
            'id':'ITEM0022',
            'name': '凉皮',
            'price': 8,
            'is_half_price': True  # 是否半价
        }
    ]

}

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
    order_list = ["ITEM0001 x 1", "ITEM0013 x 2", "ITEM0022 x 1"]
    # order_list = ["ITEM0013 x 4", "ITEM0022 x 1"]
    # order_list = ["ITEM0013 x 4"]
    bestCharge(order_list)
