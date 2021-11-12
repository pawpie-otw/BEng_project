import random
from typing import Any, Optional, Tuple
from app.data.population import gender_enum
import pandas as pd
import json
from data import population as pop


class People:
    path_dict = {
        "f_fname": r"data/first_name_female_living_10k.csv",
        "f_lname": r'data/last_name_female_living_2020_10k.csv',
        "m_fname": r"data/first_name_male_living_10k.csv",
        "m_lname": r"data/last_name_male_living_2020_10k.csv",
        "age": r"'data/population.json'"
    }

    @staticmethod
    def generate_dataset(self, n: int = 1):

        # load all datasets using in generate people dataset
        f_fname_df = pd.read_csv(self.path_dict["f_fname"])
        f_lname_df = pd.read_csv(self.path_dict["f_lname"])
        m_fname_df = pd.read_csv(self.path_dict["m_fname"])
        m_lname_df = pd.read_csv(self.path_dict["m_lname"])
        pop_age = pd.read_json(self.path_dict['age'])

        # drawing gender and fitting other datasets
        if (gender_ := self.__draw_sex()) == gender_enum.FEMALE:
            names = self.draw_from_df((f_fname_df.value, f_lname_df.value),
                                      (f_fname_df.amount, f_lname_df.amount))
            age = pop
        elif gender_ == gender_enum.MALE:
            names = self.draw_from_df((m_fname_df.value, m_lname_df.value),
                                      (m_fname_df.amount, m_lname_df.amount))

    @staticmethod
    def draw_from_df(*args: Tuple[Tuple[float]]):
        return (random.choices(d_set[0], d_set[1])
                for d_set in args)

    @staticmethod
    def __draw_gender(gender: Tuple[Any] = (gen for gen in gender_enum),
                      chance: Tuple[float] = (pop.gender_chance_enum.FEMALE.value,
                                              pop.gender_chance_enum.MALE.value)) -> Any:
        """draw sex of people base on given chance for each one

        Args:
            symbols (Optional[Tuple], optional): representation of each sex. Defaults to ('f', 'm').
            chance (Optional[Tuple[float]], optional): chance to draw every option. Defaults to (population_enum.SEX_FEMALE.value, population_enum.SEX_MALE.value).

        Returns:
            Any: one of value given in symbols, default char.
        """
        return random.choices(gender, chance)[0]

    @staticmethod
    def __draw_str_from_file(dataset: Tuple, k: Optional[int] = 1) -> str:
        """draw k from files and return them based on number in second column which is scaled to percent as chance to draw.

        Args:
            file_name ([type]): path to file with data.
            k (Optional[int]): amount of selected queries. Defaults to 1.

        Returns:
            np.array: [description]
        """
        df = pd.read_csv(file_name)
        return random.choices(df["name"], weights=df['amount'], k=k)

    @staticmethod
    def draw_growth():

        pass


if __name__ == '__main__':
    Person.generate_data(n=100)
