from pydantic import BaseModel, EmailStr, model_validator


class UserRegisterSchema(BaseModel):
    login: str
    email: EmailStr
    password: str
    password_2: str

    @model_validator(mode="after")
    def validate_data(self):
        if self.password != self.password_2:
            raise ValueError("Пароли не совпадают")

        if len(self.login) < 3:
            raise ValueError("Логин должен быть минимум 3 символа")

        return self


class UserLoginSchema(BaseModel):
    login: str
    password: str


class TokenRefreshSchema(BaseModel):
    refresh_token: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponseSchema(BaseModel):
    id: int
    login: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool

    class Config:
        from_attributes = True