import time
import random
import string
from car import Car
from retailer import Retailer
from car_retailer import CarRetailer
from order import Order


# 2.5 Main File
# 2.5.1
def main_menu():
	print("""
	Menu
     a) Look for the nearest car retailer
     b) Get car purchase advice
     c) Place a car order
     d) Exit
	""")

# 2.5.2
def generate_test_data():
	# generate random car objects
    cars = []
    for car in range(12):  # 12 cars
        car_code = "".join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(100000, 1000000))
        car_name = "".join(random.choices(string.ascii_letters, k=25))
        car_capacity = random.randint(4, 30)
        car_horsepower = random.randint(100, 300)
        car_weight = random.randint(1500, 3000)
        car_type = random.choice(["FWD", "RWD", "AWD"])
        cars.append(Car(car_code, car_name, car_capacity, car_horsepower, car_weight, car_type))

    # generate random retailers objects
    retailers = []
    addresses = ["Wellington Rd Clayton, VIC3168", "Wellington Rd Clayton, VIC3168",
                 "Clayton Rd Mount Waverley, VIC3170"]
    for index in range(3):   # 3 car retailers
        retailer_id = random.randint(10000000, 100000000)
        retailer_name = "".join(random.choices(string.ascii_letters, k=10))
        carretailer_address = addresses[index]
        carretailer_business_hours = ()
        while True:  # validate business hour
            temp_business_hours = (random.randint(60, 230) / 10, random.randint(60, 230) / 10)
            if temp_business_hours[0] < temp_business_hours[1]:   # check if opening time < closing time
                carretailer_business_hours = temp_business_hours
                break
        temp_carretailer = []
        for j in range(4):  # 4 cars
            temp_carretailer.append(cars[j + index * 4].__str__())
            carretailer_stock = temp_carretailer
        retailers.append(CarRetailer(retailer_id, retailer_name, carretailer_address, carretailer_business_hours,
                                     carretailer_stock))
    with open("../data/stock.txt", "w", encoding="utf-8") as file:
        for retailer in retailers:
            temp_str = retailer.__str__()
            temp_car_list = []
            retailer_info = temp_str[0:temp_str.find("[")]
            cars_list_info = temp_str[temp_str.find("["):]
            for j in range(len(cars_list_info.split(","))):
                cur_id = cars_list_info.split(",")[j]
                temp_id = cur_id.replace("[", "").replace("]", "").replace("'", "").strip()
                for car in cars:
                    if temp_id == car.car_code:
                        temp_car_list.append(car)
            final_car_list = [str(x) for x in temp_car_list]  # convert list to string
            final_string = retailer_info + str(final_car_list)
            file.write(final_string + "\n")  # save to the stock file


# 2.5.3
def main():
    retailers = []
    cars = []
    generate_test_data() #todo
    with open("../data/stock.txt", "r", encoding="utf-8") as file:
        content = file.readlines()
        for line in content:   # iterate every line of the stock file
            retailer_info = line.strip().split(", ")   # get retailer basic information and stock
            retailer_id = int(retailer_info[0])
            retailer_name = retailer_info[1]
            carretailer_address = ", ".join(retailer_info[2:4])
            carretailer_business_hours = (float(retailer_info[4].strip("(")), float(retailer_info[5].strip(")")))
            car_info = retailer_info[6:]  # car stock information
            carretailer_stock = []   # list of car code
            for j in range(4):   # generate car objects
                car_code = car_info[0 + j * 6].replace("[", "").replace("'", "").strip()
                car_name = car_info[1 + j * 6].strip()
                car_capacity = car_info[2 + j * 6].strip()
                car_horsepower = car_info[3 + j * 6].strip()
                car_weight = car_info[4 + j * 6].strip()
                car_type = car_info[5 + j * 6].replace("'", "").strip()
                carretailer_stock.append(car_code) # list of car code
                cars.append(Car(car_code, car_name, car_capacity, car_horsepower, car_weight, car_type)) # car object
            temp_retailer = CarRetailer(retailer_id, retailer_name, carretailer_address, carretailer_business_hours, carretailer_stock) # retailer object
            retailers.append(temp_retailer) # list of retailer objects

        print("Welcome to Car Purchase Advisor System!")

    while True:
        main_menu()
        user_input = input("Please enter your choice: ")

        if user_input == "a":
            user_postcode = ""
            while True:
                user_postcode = input("Enter your postcode: ")
                if not user_postcode.isdigit() or len(user_postcode) != 4:
                    print("Error: Invalid postcode format! Please re-enter your postcode.")
                else:
                    break
            distances = []
            for retailer in retailers:
                distances.append(retailer.get_postcode_distance(user_postcode))
            # Get the minimum distance and the corresponding retailer
            nearest_retailer = retailers[distances.index(min(distances))]
            # Display the nearest retailer
            print("Nearest retailer:", nearest_retailer.retailer_name)

        elif user_input == "b":
            selected_retailer = CarRetailer()   # selected retailer by user
            for retailer in retailers:   # display all the retailer information
                print(retailer)
            user_retailer_id = ""
            while True:
                user_retailer_id = input("Please select a Car Retailer by retailer ID: ")
                if not user_retailer_id.isdigit() or len(user_retailer_id) != 8:  # invalid input, not digit and invalid length
                    print("Error: Invalid retailer ID! Please re-enter.")
                else:
                    flag = False  # check if input retailer_id exists
                    for retailer in retailers:
                        if int(user_retailer_id) == retailer.retailer_id:
                            flag = True
                            break
                    if flag:
                        break
                    else:
                        print("Error: Retailer ID doesn't exist! Please re-enter.")
            for retailer in retailers: # iterate every line in the retailer
                if int(user_retailer_id) == retailer.retailer_id:
                    print(retailer)
                    selected_retailer = retailer  # assign to selected retailer
                    break

            while True:
                print("""Options:
i) Recommend a car
ii) Get all cars in stock
iii) Get cars in stock by car types
iv) Get probationary licence permitted cars in stock
                """)

                user_option = input("Please select your option: ")
                if user_option not in ["i", "ii", "iii", "iv"]:
                    print("Error: Invalid option! Please select again.")

                if user_option == "i":
                    recommended_car = selected_retailer.car_recommendation()
                    print("Recommended Car:", recommended_car)
                    break
                elif user_option == "ii":
                    print("Retailer ID:", selected_retailer.retailer_id)
                    print("Retailer Name: ", selected_retailer.retailer_name)
                    print("Car's Info:" )
                    car_obj_list = selected_retailer.get_all_stock()  # get all the car stock information
                    for car in car_obj_list:   # iterate every line of car stock information
                        print("\t\t" + str(car))  # display all the car objects
                    break

                elif user_option == "iii":
                    car_type_list = ["FWD", "RWD", "AWD"]  # a list of all car type
                    print("Retailer ID: ", selected_retailer.retailer_id)
                    print("Retailer Name: ", selected_retailer.retailer_name)
                    print("Car's Info: ")
                    car_obj_list = selected_retailer.get_all_stock()  # get all the car stock information
                    for car_type in car_type_list:  # iterate car type list
                        print("\t Car type:", car_type)
                        for car in car_obj_list:  # iterate every line of car stock information
                            if car_type.strip() == car.car_type.strip():
                                print("\t\t" + str(car))  # display all the car objects by car type
                    break
                elif user_option == "iv":
                    for car in selected_retailer.get_all_stock():  # iterate every line of car stock information
                        if not car.probationary_licence_prohibited_vehicle():  # check if forbidden
                            print(str(car))
                    break

        elif user_input == "c":
            selected_retailer = CarRetailer()
            user_choice = ""
            while True:
                user_choice = input("Please enter retailer ID and car code: ")
                if len(user_choice.split()) != 2:  # input: retailer_id car_code
                    print("Invalid input!")
                elif not user_choice[0].isdigit():
                    print("Retailer ID should be an 8-digit integer.")
                else:
                    flag = False
                    for retailer in retailers:  # iterate every line of retailer information
                        if int(user_choice.split()[0]) == retailer.retailer_id:  # check if input retailer_id exists
                            for car in retailer.get_all_stock():  # iterate every line of car stock information
                                if user_choice.split()[1] == car.car_code:  # check if input car_code exists
                                    flag = True
                    if flag:
                        retailer_id = user_choice.split()[0]
                        car_code = user_choice.split()[1]
                        for retailer in retailers:
                            if int(retailer_id) == retailer.retailer_id:
                                selected_retailer = retailer  # assign to the selected retailer
                        hour = time.strftime("%H")
                        minute = time.strftime("%M")
                        cur_hour = float(str(round(int(hour))) + str(round(int(minute) / 60, 2))[1:])
                        # Check if the retailer is opening for business
                        if (cur_hour < selected_retailer.carretailer_business_hours[0] or cur_hour > selected_retailer.carretailer_business_hours[1]):
                            print("Error: Out of business hours.")
                        else:
                            break
                    else:
                        print("Error: Retailer ID or car code doesn't exist! Please re-enter.")

            selected_retailer.create_order(car_code)    # call create_order function
            print("Ordered successfully!")

        elif user_input == "d":  # exit the system
            print("Thank you for using our system! ")
            break
        else:  # user input not in ["a", "b", "c", "d"]
            print("Invalid input! ")


if __name__ == "__main__":
    main()


