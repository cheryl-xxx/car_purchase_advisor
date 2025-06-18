import random
import time
import string
from car import Car
from car_retailer import CarRetailer

# 2.4 Order Class
class Order:
    # 2.4.1
    def __init__(self, order_id="", order_car= Car(), order_retailer=CarRetailer(),
                order_creation_time=round(time.time())):
        self.order_id = order_id
        self.order_car = order_car
        self.order_retailer = order_retailer
        self.order_creation_time = order_creation_time

    # 2.4.2
    def __str__(self):
        return (f"{self.order_id}, {self.order_car.car_code}, {self.order_retailer.retailer_id},"
                f"{self.order_creation_time}")

    # 2.4.3
    def generate_order_id(self, car_code):
        str_1 = "~!@#$%^&*"
        # step 1
        random_str = "".join(random.choices(string.ascii_lowercase, k=6))   # string with 6 lowercase char
        # step 2
        str_2 = ""
        for j in range(len(random_str)):
            if j % 2 == 1:   # 2nd, 4th, 6th
                str_2 += random_str[j].upper()
            else:
                str_2 += random_str[j]
        # step 3
        list_3 = []
        for j in str_2:
            list_3.append(ord(j))  # get ascii code
        # step 4
        list_4 = []
        for j in list_3:
            list_4.append((j ** 2) % len(str_1))
        # step 5
        list_5 = []
        for j in list_4:
            list_5.append(str_1[j])
        # step 6
        str_6 = str_2
        for j in range(len(str_2)):
            str_6 += list_5[j] * j
        # step 7
        str_7 = str_6
        str_7 += str(car_code) + str(self.order_creation_time)
        return str_7
