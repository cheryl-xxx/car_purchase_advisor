import random

# 2.2 Retailer Class
class Retailer:
   # 2.2.1
   def __init__(self, retailer_id=-1, retailer_name="CHANG SZ"):
       self.retailer_id = retailer_id
       self.retailer_name = retailer_name

   # 2.2.2
   def __str__(self):
       return f"{self.retailer_id}, {self.retailer_name}"

   # 2.2.3
   def generate_retailer_id(self, list_retailer=[]):
       # iterate all the existing retailers' id
       list_retailer = [retailer.retailer_id for retailer in list_retailer]
       new_id = random.randint(10000000, 100000000)
       # check if new_id exists
       while True:
           if new_id in list_retailer:
               new_id = random.randint(10000000, 100000000)
           else:
               self.retailer_id = new_id
               break





# test code
# test_retailer =Retailer()
# print(test_retailer.generate_retailer_id())