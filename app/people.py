from random import randint, choices
from typing import Any, Optional, Tuple, Annotated

from pandas.core.frame import DataFrame
from data.people.population import gender_enum
import pandas as pd
from data.people import population as pop
from common_functions.custom_draws import draw_from_df


class People:
    """class to generate a dataset

    Returns:
        [type]: [description]
    """
    path_dict = {
        "f_fname": r"data/people/first_name_female_living_10k.csv",
        "f_lname": r'data/people/last_name_female_living_2020_10k.csv',
        "m_fname": r"data/people/first_name_male_living_10k.csv",
        "m_lname": r"data/people/last_name_male_living_10k.csv",
        "voivodship_males": r"data/voivodship_males_by_sexage.csv",
        "voivodship_females": r"data/voivodship_females_by_sexage.csv",
        "age": r"data/people/population.json"
    }

    @staticmethod
    def generate_dataset(n: int = 1,
                         number_of_names: int = 1,
                         age_low_lim: int = 0,
                         age_up_lim: int = 100,
                         only_males: bool = False,
                         only_females: bool = False,
                         number_of_fnames: int = 1,
                         unregular_number_of_names: bool = False,
                         double_surnames: bool = False,
                         unregular_double_surname: bool = False) -> pd.DataFrame:

        # load all datasets using in generate people dataset
        f_fname_df = pd.read_csv(__class__.path_dict['f_fname'])
        f_lname_df = pd.read_csv(__class__.path_dict["f_lname"])
        m_fname_df = pd.read_csv(__class__.path_dict["m_fname"])
        m_lname_df = pd.read_csv(__class__.path_dict["m_lname"])
        voivodship = {"males": pd.read_csv(__class__.path_dict["voivodship_males"]),
                      "females": pd.read_csv(__class__.path_dict["voivodship_females"])}
        pop_age = pd.read_json(__class__.path_dict['age'])

        result = pd.DataFrame()
        lnames_num = 2 if double_surnames else 1

        if only_females:
            result['gender'] = pd.Series(
                ['female' for _ in range(n)]).astype("category")

            result['first name'] = __class__.__draw_names(
                result, f_fname_df, None, number_of_fnames, unregular_number_of_names)

            result['last name'] = __class__.__draw_names(
                result, f_lname_df, None, lnames_num, unregular_double_surname, name_separator="-")

            result['age'] = result.apply(
                lambda x: choices(range(101), pop_age['female'])[0], axis=1)

        elif only_males:
            result['gender'] = pd.Series(
                ['male' for _ in range(n)]).astype("category")
            result['first name'] = __class__.__draw_names(
                result, m_fname_df, None, number_of_fnames, unregular_number_of_names)
            result['last name'] = __class__.__draw_names(
                result, m_lname_df, None, lnames_num, unregular_double_surname, name_separator="-")
            result['']

        # DEFAULT WAY

        # drawing a gender
        result['gender'] = pd.Series([__class__.__draw_gender().value
                                      for _ in range(n)]).astype("category")

        # drawing a first names
        result['first name'] = __class__.__draw_names(
            result, f_fname_df, m_fname_df, number_of_fnames, unregular_number_of_names)

        # drawing a last name
        result['last name'] = __class__.__draw_names(
            result, f_lname_df, m_lname_df, lnames_num, unregular_double_surname, name_separator="-")

        result['age'] = result.apply(
            lambda x: choices(range(101), pop_age[x.gender])[0], axis=1)

        result['voivodship'] = result.apply(
            lambda x: __class__.__draw_voivodship(
                x.age, voivodship[str(x.gender)+"s"]), axis=1
        )

        # result["height"] +=
        # result["weight"] +=

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
        return choices(gender, chance)[0]

    @ staticmethod
    def __draw_names(df: pd.DataFrame,
                     first_names_set: pd.DataFrame,
                     second_names_set: pd.DataFrame = None,
                     number_of_names: int = 1,
                     unregular_number_of_names: bool = False,
                     name_separator: Annotated[str, 1] = " ") -> pd.Series:

        # usually one is used when u choosed one gender
        if not isinstance(second_names_set, pd.DataFrame):
            if (unregular_number_of_names is None):
                return df.apply(lambda _: name_separator.join(draw_from_df(first_names_set, k=randint(1, number_of_names))[0]))
            return df.apply(lambda _: name_separator.join(draw_from_df(first_names_set, k=number_of_names)[0]), axis=1)

        # random (1:number of names) number of names
        if unregular_number_of_names and (number_of_names > 1):
            return df.apply(lambda x: name_separator.join(draw_from_df(first_names_set, k=randint(1, number_of_names))[0])
                            if x.gender == 'female'
                            else name_separator.join(draw_from_df(second_names_set, k=randint(1, number_of_names))[0]), axis=1)

        # constant number of names
        return df.apply(lambda x: name_separator.join(draw_from_df(first_names_set, k=number_of_names)[0])
                        if x.gender == 'female'
                        else name_separator.join(draw_from_df(second_names_set, k=number_of_names)[0]), axis=1)

    def __draw_voivodship(age: int = None, voivodeship_population_dataset: pd.DataFrame = None, equal_weight: bool = False) -> str:
        """Draw and return name of polish voivodship based on population (which is equal to weight in drawing) that
        the ``voivodeship_population_dataset`` arg containts.

        Args:
            ``age`` (int): Age of person to whom the result will be matched.
            ``voivodeship_population_dataset`` (pd.DataFrame): df containts population group by age and voivodship.
            ``equal_weight`` (bool, optional): If true, population doesn't matter - every choice is equal. Defaults to False.

        Returns:
            (str): Name of voivodship in Poland.
        """
        voivodships = ['DOLNOŚLĄSKIE', 'KUJAWSKO-POMORSKIE', 'LUBELSKIE', 'LUBUSKIE',
                       'ŁÓDZKIE', 'MAŁOPOLSKIE', 'MAZOWIECKIE', 'OPOLSKIE', 'PODKARPACKIE',
                       'PODLASKIE', 'POMORSKIE', 'ŚLĄSKIE', 'ŚWIĘTOKRZYSKIE',
                       'WARMIŃSKO-MAZURSKIE', 'WIELKOPOLSKIE', 'ZACHODNIOPOMORSKIE']

        if equal_weight:
            return choices(voivodships)[0]

        age_ = age if age <= 85 else 85
        if (age is not None) and (voivodeship_population_dataset is not None):
            return choices(voivodeship_population_dataset.columns,
                           voivodeship_population_dataset.iloc[age_])[0]

    def test_voivodship(age: int = None, voivodeship_population_dataset: pd.DataFrame = None, equal_weight: bool = False):
        return __class__.__draw_voivodship(age=age, voivodeship_population_dataset=voivodeship_population_dataset, equal_weight=equal_weight)

    @ staticmethod
    def __single_gender() -> pd.DataFrame:
        pass


if __name__ == '__main__':
    res = People.generate_dataset(n=20)
    print(res)
    # voivodship = {"males": pd.read_csv(People.path_dict["voivodship_males"]),
    #               "females": pd.read_csv(People.path_dict["voivodship_females"])}
    # print(People.test_voivodship(10, voivodship["male"+"s"]))
