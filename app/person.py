import random
from typing import Any, Optional, Tuple
from data.population import gender_enum
import pandas as pd
from data import population as pop
from common_functions.custom_draws import draw_from_df


class People:
    """class to generate a dataset

    Returns:
        [type]: [description]
    """
    path_dict = {
        "f_fname": r"data/first_name_female_living_10k.csv",
        "f_lname": r'data/last_name_female_living_2020_10k.csv',
        "m_fname": r"data/first_name_male_living_10k.csv",
        "m_lname": r"data/last_name_male_living_10k.csv",
        "age": r"data/population.json"
    }

    @staticmethod
    def generate_dataset(n: int = 1):

        # load all datasets using in generate people dataset
        f_fname_df = pd.read_csv(__class__.path_dict['f_fname'])
        f_lname_df = pd.read_csv(__class__.path_dict["f_lname"])
        m_fname_df = pd.read_csv(__class__.path_dict["m_fname"])
        m_lname_df = pd.read_csv(__class__.path_dict["m_lname"])
        pop_age = pd.read_json(__class__.path_dict['age'])

        result = []

        for _ in range(n):
            # drawing gender and fitting datasets to it
            if (gender_ := __class__.__draw_gender()) == gender_enum.FEMALE:
                names_ds = draw_from_df(f_fname_df, f_lname_df)

            elif gender_ == gender_enum.MALE:
                names_ds = draw_from_df(m_fname_df, m_lname_df)

            # drawing names
            # names = draw_from_df(
            #     (names_ds[0].name), (names_ds[1].amount))

            # drawing age
            age: int = random.choices(range(101), pop_age[gender_.value])[0]

            result.append((gender_.value[0], age, *names_ds))
        return result

    @ staticmethod
    def __draw_gender(gender: Tuple[Any] = tuple(gen for gen in gender_enum),
                      age_low_lim: Optional[int] = 0, age_up_lim: Optional[int] = 100,
                      chance: Tuple[float] = (pop.gender_chance_enum.FEMALE.value,
                                              pop.gender_chance_enum.MALE.value),) -> Any:
        """draw gender of people base on given chance for each one

        Args:
            symbols (Optional[Tuple], optional): representation of each sex. Defaults to ('f', 'm').
            chance (Optional[Tuple[float]], optional): chance to draw every option. Defaults to (population_enum.SEX_FEMALE.value, population_enum.SEX_MALE.value).

        Returns:
            Any: one of value given in symbols, default char.
        """
        return random.choices(gender, chance)[0]

    @ staticmethod
    def draw_growth():

        pass
