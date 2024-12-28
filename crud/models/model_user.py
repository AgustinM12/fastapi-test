from pydantic import BaseModel, Field, field_validator
from typing import Optional


# TODO: REALIZAR MODELOS DE PYDANTIC
# TODO: AGREGAR VALIDACIONES A LOS MODELOS 
class User(BaseModel):
    id: Optional[str]
    name: str = Field(min_length=5, max_digits=15)
    email: str
    password: str = Field(default=0000)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123",
                "name": "Messi",
                "email": "messi@email.com",
                "password": "123",
            }
        }
    }
    
    @field_validator('name')
    def validate_name(cls, value):
        if len(value) < 5:
            raise ValueError("El nombre debe tener mas de 5 caracteres")
        if len(value) > 15:
            raise ValueError("El nombre debe tener menos de 15 caracteres")
        return value

# TODO: VALIDACIONES NUMERICAS
# gt - greater than
# ge - greater than or equal
# lt - less than
# le - less than or equal
