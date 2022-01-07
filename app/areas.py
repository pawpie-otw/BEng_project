import pandas as pd

from random import choice,choices
from json import load


class Areas:
    path_dict = {
        "voivodship_males": r"data/areas/voivodship_males_by_sexage.csv",
        "voivodship_females": r"data/areas/voivodship_females_by_sexage.csv",
        "postcodes": r"data/areas/post_codes.json"
    }


    @classmethod
    def generate_dataset(cls, base_df: pd.DataFrame = None, voivodship:bool = True, postcode:bool = True,
                        equal_voivodeship:bool = False, equal_postcode:bool = False, n: int = None):
        """Return data related to areas - voivodeship and postcode.

        Args:
            base_df (pd.DataFrame): DF which contain base data to generate rest of [data]. No needed if n.
            voivodship (bool, optional): If `True` - generate voivodeship data. Defaults to True.
            postcode (bool, optional): If `True` - generarate postcode data. Defaults to True.
            equal_voivodeship (bool, optional): If `True` - no based on `base_df`, draw randomly voivodeship. Defaults to False.
            equal_postcode (bool, optional): If `True` - no based on `voivodeship` data, draw randomly postcode. Defaults to False.
            n (int, optional): needed if `base_df` = `None`. Then return randomly drawn `voivodeship` (<=> `equal_voivodeship` = `True`) or
            randomly drawn `postcode` (<=> `equal_postcode` = `True` if `voivodship` = `False`).

        Returns:
            pd.DataFrame: return choosen data with given (or default) options.
        """

        voivodship_data = {"males": pd.read_csv(cls.path_dict["voivodship_males"]),
                    "females": pd.read_csv(cls.path_dict["voivodship_females"])}
        postcodes_data = dict(load(open(cls.path_dict["postcodes"], encoding="utf8")))
        
        result = dict()

        if (base_df is None) and isinstance(n, int):
            if n<1:
                pass # raise exception bad value

            if voivodship:
                result["voivodeship"] = pd.Series([cls.generate_voivodeship(equal_weight=True)
                                                for _ in range(n)])
            if postcode:
                if not voivodship or equal_postcode:
                    result["postcode"] = pd.Series([cls.generate_postcode(postcodes_data, no_dependence=True)
                                                    for _ in range(n)])
                else:
                    result["postcode"] = result["voivodeship"].apply(lambda x: cls.generate_postcode(postcodes_data,dependence=x))

        elif voivodship:
            result["voivodeship"] = base_df.apply(lambda x: cls.generate_voivodeship(x.age, voivodship_data[str(x.gender)+"s"], equal_weight=equal_voivodeship), axis=1)
            
            if postcode:
                result["postcode"] = result["voivodeship"].apply(lambda x: cls.generate_postcode(
                                                                postcodes_data, x, no_dependence=equal_postcode
                                                                ))
        elif postcode :
            result["postcode"] = base_df.apply(lambda x: cls.generate_postcode(postcodes_data, no_dependence=True))

        return pd.DataFrame(result)
        

    @staticmethod
    def generate_postcode(dataset:dict, dependence:str=None, no_dependence:bool=False)->str:
        """Return postcode which depends on  given voivodeship (if `dependence` not None)
        or randomly (if `no_dependence=True`).

        Args:
            dataset (dict): dict build as {voivodeship_name:[postcode0,postcode1 ...],}
            dependence (str, optional): the value (voivodeship name) on which the result depends. 
            no_dependence (bool, optional): if True, then no needed `dependence` value - result is drawn randomly.

        Returns:
            str: polish post-code
        """
        if no_dependence:
            return choice(dataset[choice(tuple(dataset.keys()))])
        return choice(dataset[dependence])
        

    @staticmethod
    def generate_voivodeship(age: int = None, voivodeship_population_dataset: pd.DataFrame = None, equal_weight: bool = False) -> str:
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