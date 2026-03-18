from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated


class Address(BaseModel):
    
    city: str
    state: str
    pin: str


class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name within 50 characters', examples=['Akshata', 'John Doe'])]
    address: Address
    email: EmailStr
    linkedin_url: AnyUrl
    age: int= Field(gt=0, lt=100)
    weight: Annotated[float, Field(gt=0, strict=True)] #kgs
    height: Annotated[float, Field(gt=0, strict=True)] #cm
    married: Annotated[bool, Field(default=None, description='Is the patient married or not?')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_info: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains=['hdfc.com', 'icici.com']
        domain_name=value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        return value.upper()
    

    @field_validator('age', mode='before')
    @classmethod
    def age_validator(cls, value):
        if 0<value<100:
            return value
        else:
            raise ValueError('Age must be between 0 and 100')
        
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age>60 and 'emergency' not in model.contact_info:
            raise ValueError('Patients above 60 must have an emergency contact')
        else:
            return model
        
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi= round(self.weight/self.height**2, 2)
        return bmi

address_dict= {'city': 'Pune', 'state': 'Maharashtra', 'pin': '411001'}

address_1= Address(**address_dict)


def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.address)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.married)
    print('BMI', patient.calculate_bmi)
    print("inserted")

patient_info= {'name': 'Akshata', 'address': address_1, 'email': 'akshata@hdfc.com', 'linkedin_url': 'https://www.linkedin.com/in/akshata', 'age': 65, 'weight': 51.5, 'height': 1.55, 'married': True, 'contact_info': {'phone': '123-456-7890', 'emergency': '0123456'}}

patient1= Patient(**patient_info)

insert_patient_data(patient1)

temp=patient1.model_dump(exclude={'address': {'state'}})
print(temp)
print(type(temp))