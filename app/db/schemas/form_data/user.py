from dataclasses import dataclass

from fastapi import Form


@dataclass
class UserBaseFD:
    fam: str = Form(...)
    name: str = Form(...)
    otc: str = Form(...)
    email: str = Form(...)  # Написать валидатор с помощью regex
    phone: str = Form(...)  # Написать валидатор с помощью regex
