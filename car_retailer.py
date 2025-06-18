import time
import random
from car import Car
from retailer import Retailer


# 2.3 CarRetailer Class
class CarRetailer(Retailer):
    # 2.3.1
    def __init__(self, retailer_id="-1", retailer_name="CHANG SZ",
                 carretailer_address="Wellington Road Clayton, VIC 3800",
                 carretailer_business_hours=(8.5, 17.5),
                 carretailer_stock=[]):
        super().__init__(retailer_id, retailer_name)  # inherits from Retailer class
        self.carretailer_address = carretailer_address
        self.carretailer_business_hours = carretailer_business_hours
        self.carretailer_stock = carretailer_stock

    # 2.3.2
    def __str__(self):
        return (f"{self.retailer_id}, {self.retailer_name}, {self.carretailer_address}, "
                f"{self.carretailer_business_hours}, {self.carretailer_stock}")

    # 2.3.3
    def load_current_stock(self, path):
        cars_list = []
        with open(path, "r", encoding="utf-8") as file:  # open and read stock.txt file
            retailer_info = file.readlines()
        for line in retailer_info:  # iterate every line of stock.txt file
            # get carretailer information according to retailer_id
           if self.retailer_id == int(line.split(",")[0]): # retailer_id
               # get all the car information from the retailer stock
               all_car_info = line.split("[\'")[1].strip("\n").strip("]").strip("\'")
               first_car_code = all_car_info.split(",")[0]   # 1st car code
               other_car_code = all_car_info.split("\', \'")   # remaining car code
               # get all the car codes and save to the empty list
               for j in other_car_code:
                   cars_list.append(j.split(",")[0])
        self.carretailer_stock = cars_list

    # 2.3.4
    def is_operating(self, cur_hour):
       if cur_hour >= self.carretailer_business_hours[0] and cur_hour <= self.carretailer_business_hours[1]:
           return True
       else:
           return False

    # 2.3.5
    def get_all_stock(self):
        car_list = []
        with open("../data/stock.txt", "r", encoding="utf-8") as file:   # open and read stock.txt file
            content = file.readlines()
        for line in content:   # iterate every line of stock.txt file
            # get carretailer information according to retailer_id
            if self.retailer_id == int(line.split(",")[0]):
                # get all the car information from the retailer stock
                all_car_info = line.split("[\'")[1].strip("\n").strip("]").strip("\'")
                first_car_code = all_car_info.split(",")[0]  # 1st car code
                other_car_code = all_car_info.split("\', \'")  # remaining car code
                for j in other_car_code:  # iterate all the car code in stock
                    car_code = j.split(",")[0]
                    car_name = j.split(",")[1]
                    car_capacity = j.split(",")[2]
                    car_horsepower = j.split(",")[3]
                    car_weight = j.split(",")[4]
                    car_type = j.split(",")[5]
                    # get car objects and save to the empty list
                    test_car = Car(car_code, car_name, car_capacity, car_horsepower,
                                   car_weight, car_type)
                    car_list.append(test_car)
        return car_list

    # 2.3.6
    def get_postcode_distance(self, postcode):
        # get postcode from carretailer_address
        user_postcode = int(self.carretailer_address[-4:])
        difference = abs(int(postcode) - user_postcode)
        return difference

    # 2.3.7
    def remove_from_stock(self, car_code):
        new_stock_info = ""
        remove_flag = False  # if the removal is successful, return True
        with open("../data/stock.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:  # iterate every line from stock file
                # find the retailer
                if int(line.split(",")[0]) == self.retailer_id:
                    cars_info = line.split("['")[1].strip("\n").strip("]").strip("'")
                    cars_list = cars_info.split("', '")
                    old_cars_list = str(cars_list)
                    # get car infomation according to car code, and remove from list
                    for car_index in range(len(cars_list)):
                        if car_code in cars_list[car_index]:
                            cars_list.pop(car_index)
                            new_cars_list = str(cars_list)
                            remove_flag = True
                            break
                    if remove_flag: # if removal successful
                        new_stock_info = new_stock_info + line.replace(old_cars_list, new_cars_list)
                    else:
                        new_stock_info = new_stock_info + line
                else:
                    # if != retailer_id, no change to the file
                    new_stock_info = new_stock_info + line
        if remove_flag: # write back to the file
            with open("../data/stock.txt", "w", encoding="utf-8") as file:
                file.write(new_stock_info)
            self.load_current_stock("../data/stock.txt")
            return True
        else:
            return False

    # 2.3.8
    def add_to_stock(self, car):
        # get retailer information from the stock file
        new_stock_info = ""
        add_flag = False  # if the adding is successful, return True
        with open("../data/stock.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:  # get single line from txt file
                # find the retailer
                if int(line.split(",")[0]) == self.retailer_id:
                    cars_info = line.split("['")[1].strip("\n").strip("]").strip("'")
                    cars_list = cars_info.split("', '")
                    old_cars_list = str(cars_list)
                    # get car infomation according to car code, and remove from list
                    for car_index in range(len(cars_list)):
                        if car.car_code not in cars_list[car_index]:
                            cars_list.append(car_index)
                            new_cars_list = str(cars_list)
                            add_flag = True
                            break
                    if add_flag:
                        new_stock_info = new_stock_info + line.replace(old_cars_list, new_cars_list)
                    else:
                        new_stock_info = new_stock_info + line
                else:
                    # if != retailer_id, no change to the file
                    new_stock_info = new_stock_info + line
        if add_flag:
            with open("../data/stock.txt", "w", encoding="utf-8") as file:
                file.write(new_stock_info)
            self.load_current_stock("../data/stock.txt")
            return True
        else:
            return False

    # 2.3.9
    def get_stock_by_car_type(self, car_types):
        result = []
        with open("../data/stock.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:  # iterte every line from stock file
                # find the retailer according to retailer id
                if int(line.split(",")[0]) == self.retailer_id:
                    cars_info = line.split("['")[1].strip("\n").strip("]").strip("'")
                    cars_list = cars_info.split("', '")
                    for j in cars_list:
                        car_type = j.split(",")[-1].strip(" ")
                        if car_type in car_types:
                            # get car objects and save to the list
                            car_code = j.split(",")[0]
                            car_name = j.split(",")[1].strip(" ")
                            car_capacity = j.split(",")[2].strip(" ")
                            car_horsepower = j.split(",")[3].strip(" ")
                            car_weight = j.split(",")[4].strip(" ")
                            new_car = Car(car_code, car_name, car_capacity, car_horsepower,
                                          car_weight, car_type)
                            result.append(new_car)
        return result

    # 2.3.10
    def get_stock_by_licence_type(self, licence_type):
        result = []
        with open("../data/stock.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:  # iterate every line from stock file
                # find the retailer according to retailer id
                if int(line.split(",")[0]) == self.retailer_id:
                    cars_info = line.split("['")[1].strip("\n").strip("]").strip("'")
                    cars_list = cars_info.split("', '")
                    for j in cars_list:
                        car_code = j.split(",")[0]
                        car_name = j.split(",")[1].strip(" ")
                        car_capacity = j.split(",")[2].strip(" ")
                        car_horsepower = j.split(",")[3].strip(" ")
                        car_weight = j.split(",")[4].strip(" ")
                        car_type = j.split(",")[5].strip(" ")
                        car_obj = Car(car_code, car_name, car_capacity, car_horsepower,
                                      car_weight, car_type)
                        # check licence type and car status
                        if licence_type == "P" and car_obj.probationary_licence_prohibited_vehicle():
                            continue
                        else:
                            result.append(car_obj)
        return result

    # 2.3.11
    def car_recommendation(self):
        result = []
        with open("../data/stock.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:  # iterate every line from stock file
                # find the retailer according to retailer id
                if int(line.split(", ")[0]) == self.retailer_id:
                    cars_info = line.split("['")[1].strip("\n").strip("]").strip("'")
                    cars_list = cars_info.split("', '")
                    for j in cars_list:  # iterate every line of the cars in stock
                        car_code = j.split(",")[0]
                        car_name = j.split(",")[1].strip(" ")
                        car_capacity = j.split(",")[2].strip(" ")
                        car_horsepower = j.split(",")[3].strip(" ")
                        car_weight = j.split(",")[4].strip(" ")
                        car_type = j.split(",")[5].strip(" ")
                        # get car objects and save to the empty list
                        car_obj = Car(car_code, car_name, car_capacity, car_horsepower,
                                      car_weight, car_type)
                        result.append(car_obj)
        return random.choice(result)

    # 2.3.12
    def create_order(self, car_code):
        with open("../data/stock.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:  # iterate every line from stock file
                # find the retailer according to retailer id
                if int(line.split(",")[0]) == self.retailer_id:
                    cars_info = line.split("['")[1].strip("\n").strip("]").strip("'")
                    cars_list = cars_info.split("', '")
                    for j in cars_list:  # iterate every line of the cars in stock
                        if j.split(",")[0].strip(" ") == car_code:
                            car_type = j.split(",")[-1]
                            temp_car_code = j.split(",")[0]
                            car_name = j.split(",")[1].strip(" ")
                            car_capacity = j.split(",")[2].strip(" ")
                            car_horsepower = j.split(",")[3].strip(" ")
                            car_weight = j.split(",")[4].strip(" ")
                            car_obj = Car(temp_car_code, car_name, car_capacity, car_horsepower,
                                          car_weight, car_type)
                            self.remove_from_stock(temp_car_code)  # remove from stock
                            self.load_current_stock("../data/stock.txt") # display current stock
                            from order import Order
                            order_obj = Order("", car_obj, self, round(time.time()))
                            order_obj.order_id = order_obj.generate_order_id(temp_car_code)
                            with open("../data/order.txt", "a", encoding="utf-8") as order_file:
                                order_file.write(order_obj.__str__() + "\n")     # add to the order file
                            return order_obj

