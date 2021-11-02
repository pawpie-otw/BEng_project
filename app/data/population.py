import json
import random as rd
from enum import Enum, auto
from typing import List


class sex_enum(Enum):
    FEMALE = "female"
    MALE = "male"


class pop_sum_enum(Enum):
    FEMALE_POP = 19762772
    MALE_POP = 18502241
    TOTAL_POP = 38265013


class pop_chance_enum(Enum):
    FEMALE = 0.5164710645727469
    MALE = 0.4835289354272531


class population:
    def draw_sex(self, symbols):
        pass

    def chance_for_sex(self, age_low_lim: int = 0,
                       age_up_lim: int = 100, chances=List[float]
                       ) -> float:
        """Return chance to draw a sex based on amount of each sex group in given age range

        Args:
            age_low_lim (int, optional): lowest limit of age. Defaults to 0.
            age_up_lim (int, optional): upper limit of age. Defaults to 100.
            group (str, optional): [description]. Defaults to "total".
            pop_group_amount (int, optional): [description]. Defaults to pop_sum_enum.TOTAL_POP.value.

        Returns:
            float: chance for draw representant of [group] (value: .0 - 1.)
        """

        return requested_group_amount/total_group_amount

    def chance_for_age(self, group: sex_enum,
                       age_low_lim: int = 0,
                       age_up_lim: int = 100) -> float:
        pass


if __name__ == '__main__':
    pop = population()
    print(pop.chance_for(20, 50, "total"))
