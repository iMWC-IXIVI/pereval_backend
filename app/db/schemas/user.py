from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    fam: str
    name: str
    otc: str
    email: EmailStr
    phone: str  # Написать валидатор для телефона с помощью регулярного выражения +7 (***) *** ** **


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
