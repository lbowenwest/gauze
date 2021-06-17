import pytest

try:
    import pydantic
except ImportError:
    pytest.skip("pydantic is not installed", allow_module_level=True)


from pydantic import BaseModel, validator, ValidationError
from gauze.collection import Collection


@pytest.mark.parametrize("values", [Collection([1, 2, 3]), [1, 2, 3], (1, 2, 3)])
def test_collection_in_model(values):
    class Model(BaseModel):
        numbers: Collection[int]

    model = Model(numbers=values)
    assert isinstance(model.numbers, Collection)


def test_pydantic_validation():
    class Model(BaseModel):
        even_numbers: Collection[int]

        @validator("even_numbers", each_item=True)
        def validate_even_numbers(cls, value):
            if value % 2 == 0:
                return value
            else:
                raise ValueError(f"{value} is not even")

    with pytest.raises(ValidationError):
        col = Model(even_numbers=[1, 2, 4, 6])


def test_constrained_model():
    class Model(BaseModel):
        even_numbers: Collection[pydantic.conint(multiple_of=2)]

    with pytest.raises(ValidationError):
        Model(even_numbers=[2, 4, 5])
