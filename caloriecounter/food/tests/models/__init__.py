# These files contain the tests for the 'food' part of the calorie counter app.
# I've split the models into two files, Unit, and the rest.
# This is because Unit's by themselves are pretty complex and extendable,
# and all other models are closely related to FoodProducts (Nutrients are always related to a FoodProduct)
from .food_product import *
from .unit import *