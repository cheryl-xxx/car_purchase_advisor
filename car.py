import math

# 2.1 Car Class
class Car:
    # 2.1.1
    def __init__(self, car_code="CB230602", car_name="CHANG", car_capacity=4,
                 car_horsepower=100, car_weight=1000, car_type="AWD"):
        self.car_code = car_code
        self.car_name = car_name
        self.car_capacity = car_capacity
        self.car_horsepower = car_horsepower
        self.car_weight = car_weight
        self.car_type = car_type

    # 2.1.2
    def __str__(self):
        return (f"{self.car_code}, {self.car_name}, {self.car_capacity}, "
                f"{self.car_horsepower}, {self.car_weight}, {self.car_type}")

    # 2.1.3
    def probationary_licence_prohibited_vehicle(self):
        power_to_mass_ratio = round(float(self.car_horsepower) / float(self.car_weight), 3) * 1000
        #check if the mass ratio value is valid
        if power_to_mass_ratio > 130:
            return True
        else:
            return False

    # 2.1.4
    def found_matching_car(self, card_code):
        if self.car_code == card_code:
            return True
        else:
            return False

    # 2.1.5
    def get_car_type(self):
        return self.car_type


# test code
# test_car = Car()
# print(test_car)