from faker import Faker 
from pandas import DataFrame

faker = Faker()

hospital = DataFrame(
    data = [
        {'id':1, 'name':'SafeCare Hospital'}
    ]
)

doctors = DataFrame(
    data = {
        'id': list(range(1,4)),
        'hospital_id': [1]*3,
        'name': ["Dr." + faker.name() for _ in range(3)]
    }
)

hospital_staffs = DataFrame(
    data = {
        'user_id': list(range(1,3)),
        'hospital_id': [1]*2
    }
)

hospital.to_csv("./resources/hospitals.csv")
doctors.to_csv("./resources/doctors.csv")
hospital_staffs.to_csv("./resources/hospital_staffs.csv")
