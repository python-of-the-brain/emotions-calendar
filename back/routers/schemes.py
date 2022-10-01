from pydantic import BaseModel, EmailStr, ValidationError, validator, Field, SecretStr

from loguru import logger

class UserRegisterScheme(BaseModel):
    
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=64)
    password2: SecretStr 


    @validator("password2")
    def validate_password2(cls, v, values):
        logger.warning(values.get('password'))
        if values.get('password').get_secret_value() != v.get_secret_value():
            raise ValueError("Must be same as pasword")
        return v


    