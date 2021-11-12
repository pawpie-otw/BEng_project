from enum import Enum
import pandas as pd


class gender_enum(Enum):
    FEMALE = "female"
    MALE = "male"


class pop_sum_enum(Enum):
    FEMALE_POP = 19762772
    MALE_POP = 18502241
    TOTAL_POP = 38265013


class gender_chance_enum(Enum):
    FEMALE = 0.5164710645727469
    MALE = 0.4835289354272531


class Population:

    @staticmethod
    def gender_chance_by_age(gender: gender_enum,
                             age_dataset: pd.DataFrame,
                             age: int) -> float:
        """Return chance to draw a sex based on amount of each sex group in given age range

        Args:
            age_low_lim (int, optional): lowest limit of age. Defaults to 0.
            age_up_lim (int, optional): upper limit of age. Defaults to 100.
            group (str, optional): [description]. Defaults to "total".
            pop_group_amount (int, optional): [description]. Defaults to pop_sum_enum.TOTAL_POP.value.

        Returns:
            float: chance for draw representant of [group] (value: .0 - 1.)
        """
        a = 100 if age > 100 else 0 if age < 0 else age

        return age_dataset[gender.value].iloc[a]/age_dataset.total.iloc[a]

    @staticmethod
    def gender_chance_by_age_between(gender: gender_enum,
                                     age_dataset: pd.DataFrame,
                                     age_low_lim: int = 0,
                                     age_up_lim: int = 100):

        ll = 0 if age_low_lim < 0 else age_low_lim
        ul = 100 if age_up_lim > 100 else age_up_lim
        return age_dataset[gender.value].iloc[ll:ul+1].sum()/age_dataset.total.iloc[ll:ul+1].sum()

    @staticmethod
    def draw_age(gender: gender_enum, age_low_lim: int = 0, age_up_lim: int = 100):
        ll = 0 if age_low_lim < 0 else age_low_lim
        ul = 100 if age_up_lim > 100 else age_up_lim


if __name__ == '__main__':

    for i in range(10, 80):
        print(Population.gender_chance_by_age(gender_enum.FEMALE, i))
        print(Population.gender_chance_by_age_between(gender_enum.MALE, i, i+5))
        print('-'*50)
