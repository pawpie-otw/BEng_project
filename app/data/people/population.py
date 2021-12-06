import enum as Enum
from enum import Enum
import pandas as pd
from typing import Optional
import common_functions.custom_exceptions as c_exc
import random


class gender_enum(Enum):
    FEMALE = "female"
    MALE = "male"


class pop_sum_enum(Enum):
    """Enum, attrs has value equal to counted persons in particular group 
    """
    FEMALE = 19_762_772
    MALE = 18_502_241
    TOTAL = 38_265_013


class gender_chance_enum(Enum):
    """Enum class, ratio for gender"""
    FEMALE = 0.5164710645727469
    MALE = 0.4835289354272531


class Population:
    """This class contains method to calculate a chance to draw a given gender based on age/range of age read from files.

    Raises:
        c_exc.ValueTooLow: [description]
        c_exc.ValueTooLow: [description]
        c_exc.ValueTooLow: [description]
        c_exc.ValueTooLow: [description]
        c_exc.InccorectLimits: [description]

    Returns:

    """
    @staticmethod
    def gender_chance_by_age(gender: gender_enum,
                             age_dataset: pd.DataFrame,
                             age: int) -> float:
        """ Calculate chance to draw given gender in given age

        Args:
            gender (gender_enum): gender 
            age_dataset (pd.DataFrame): dataset containts counted people grouped by genders and age.
            age (int): age, have to be between 0 and 100

        Returns:
            float: [description]
        """
        if age < 0:
            raise c_exc.ValueTooLow("value should be lower or equal to 0")
        elif age > 100:
            raise c_exc.ValueTooHigh("value should be higher or equal to 100")

        return age_dataset[gender.value].iloc[a]/age_dataset.total.iloc[a]

    @staticmethod
    def gender_chance_by_age_between(gender: gender_enum,
                                     age_dataset: pd.DataFrame,
                                     age_low_lim: Optional[int] = 0,
                                     age_up_lim: Optional[int] = 100) -> float:
        """ Return a chance to draw given gender in given range of age

        Args:
            gender (gender_enum): gender as Enum attribute
            age_dataset (pd.DataFrame): dataset containts counted people grouped by genders and age.
            age_low_lim (Optional[int]): lowest limit of age's range. Defaults to 0 (min).
            age_up_lim (Optional[int]): highest limit of age's range. Defaults to 100 (max).

        Returns:
            float: chance to draw given gender
        """
        if (ll := age_low_lim) < 0 or (ul := age_up_lim) < 0:
            raise c_exc.ValueTooLow("Value should be higher or equal to 0")
        elif ll > 100 or ul > 100:
            raise c_exc.ValueTooHigh("Value should be lower or equal to 100")
        elif ll > ul:
            raise c_exc.InccorectLimits(
                "Lower limit should be lower than upper limit")
        return age_dataset[gender.value].iloc[ll:ul+1].sum()/age_dataset.total.iloc[ll:ul+1].sum()

    @staticmethod
    def age_by_gender(gender: gender_enum, age_df: pd.DataFrame, age_low_lim: Optional[int] = 0, age_up_lim: Optional[int] = 100):
        """Return age base on dataset `age_df`, which should contain a 

        Args:
            gender (gender_enum): [description]
            age_df (pd.DataFrame): [description]
            age_low_lim (Optional[int], optional): [description]. Defaults to 0.
            age_up_lim (Optional[int], optional): [description]. Defaults to 100.

        Returns:
            [type]: [description]
        """
        return random.choices(range(age_low_lim, age_up_lim+1),
                              age_df[gender.value][age_low_lim:age_up_lim+1])[0]

        pass


if __name__ == '__main__':

    for i in range(10, 80):
        print(Population.gender_chance_by_age(gender_enum.FEMALE, i))
        print(Population.gender_chance_by_age_between(gender_enum.MALE, i, i+5))
        print('-'*50)
