import random
from typing import Any, Optional, Tuple
from data.population import sex_enum


class Person:

    @staticmethod
    def draw_sex(sex: Tuple[Any] = ('f', 'm'),
                 chance: Tuple[float] = (sex_enum.FEMALE.value,
                 sex_enum.MALE.value)) -> Any:
        """draw sex of people base on given chance for each one

        Args:
            symbols (Optional[Tuple], optional): representation of each sex. Defaults to ('f', 'm').
            chance (Optional[Tuple[float]], optional): chance to draw every option. Defaults to (population_enum.SEX_FEMALE.value, population_enum.SEX_MALE.value).

        Returns:
            Any: one of value given in symbols, default char.
        """
        return random.choices(sex, chance)[0]


if __name__ == '__main__':
    pass
