from controller.user_controller import add_user
from controller.product_controller import add_product
from random import uniform
from faker import Faker

fake = Faker()
for i in range(0, 100):
    add_user(fake.unique.email(), '123456', fake.first_name(), fake.first_name(), fake.address(), '123456789')
    add_product(fake.first_name(), round(uniform(100, 200), 2))