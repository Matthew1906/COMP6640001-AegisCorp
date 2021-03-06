from faker import Faker 
from pandas import DataFrame
from random import randint
from werkzeug.security import generate_password_hash

faker = Faker()

fake_names = [faker.name_male() if x%2==0 else faker.name_female() for x in range(4)]

users = DataFrame(
    data = {
        'id':list(range(1,5)),
        'name':fake_names,
        'email':[name.lower().split()[0]+'@gmail.com' for name in fake_names],
        'password':[
            generate_password_hash(
                name.lower().split()[0],
                method='pbkdf2:sha256',
                salt_length=9,
            ) 
            for name in fake_names
        ],
        'sex':[True, False]*2,
        'dob':[faker.date_of_birth(minimum_age=22, maximum_age=40) for _ in range(4)]
    }
)

users.to_csv("./resources/users.csv")