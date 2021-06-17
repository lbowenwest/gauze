import pytest

try:
    import pydantic
except ImportError:
    pytest.skip("pydantic is not installed", allow_module_level=True)


from pydantic import BaseModel, validator, ValidationError
from gauze.collection import Collection


def test_collection_in_model():
    class Model(BaseModel):
        numbers: Collection[int]

    a = Model(numbers=Collection([1, 2, 3]))
    assert a.numbers


def test_pydantic_validation():
    class Model(BaseModel):
        even_numbers: Collection[int]

        @validator("even_numbers")
        def validate_even_numbers(cls, value):
            if value % 2 == 0:
                return value
            else:
                raise ValidationError(f"{value} is not even")

    col = Model(even_numbers=[1, 2, 4, 6])
