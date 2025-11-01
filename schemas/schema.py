from pydantic import BaseModel, Field


class Dev(BaseModel):
    dev_id: int
    name: str

class Add_devs(BaseModel):
    name: str = Field(
        ...,
        min_length=5,
        max_length=25
    )
    
class Error(BaseModel):
    message: str 
    