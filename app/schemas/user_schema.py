from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    uid: str
    name: str

    class Config:
        from_orm = True


