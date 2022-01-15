import pandas as pd

from typing import Union, Dict, Any
from random import choice, randint

from common_functions.extra_funcs import fast_choices

from common_functions import custom_draws



class Athletes:

    '''Class for generating athletes dataset'''

    path_dict = {
        "sportstatus":r"data/athletes/sportstatus_chance.csv",
        "sports_per_voivodship":r"data/athletes/sports_per_voivodship.csv",
        "all_sports":r"data/athletes/all_sports.csv"
    }
    
    

    @classmethod
    def generate_dataset(cls,
                         rows: Union[None,int],
                         base_df: Union[None, pd.DataFrame] = None,
                         sportstatus:Union[None, Dict[str, Any]] = None,
                         sportdiscipline:Union[None, Dict[str, Any]] = None) -> Dict[str, pd.Series]:
        
        sportstatus_data = pd.read_csv(cls.path_dict["sportstatus"], index_col='voivodeship')
        all_sports = pd.read_csv(cls.path_dict["all_sports"])
        sports_per_voivodeship = pd.read_csv(cls.path_dict["sports_per_voivodship"])
        voivodeship_dict = __class__.create_voivodship_dict(all_sports, sports_per_voivodeship)
        result = pd.DataFrame()
            
        result["sportstatus"] = [cls.generate_sportstatus(sportstatus_data,
                                                        voivodeship,
                                                        age,                                                          
                                                        random_chance=sportstatus.get("random_chance"))
                                for age, voivodeship in zip(base_df.age, base_df.voivodeship)]
        
        
        result["sportdiscipline"] = [cls.generate_sportdiscipline(voivodeship,voivodeship_dict)
                                      if status is not None else None
                                      for status, voivodeship in zip(result.sportstatus, base_df.voivodeship)]
        
        
        return result
      
    @staticmethod
    def generate_sportdiscipline(voivodeship, voivodship_dict)-> str:
        result = custom_draws.draw_from_df(voivodship_dict[voivodeship])[0]
        return result


    @classmethod
    def create_voivodship_dict(cls, all_sports, sports_per_voivodship):
        sport_names = []
        for col in sports_per_voivodship.columns:
            sport_names.append(col)
        sport_names_series = pd.Series(sport_names)
        dfs_voivodship_dict = {}
        for index, row in all_sports.iterrows():
            dfs_voivodship_dict[row[0]] = pd.DataFrame(
                {'Name': sport_names_series, 'People': row[1:].reset_index(drop=True)})

        return dfs_voivodship_dict
    
    @classmethod
    def generate_sportstatus(cls,
                        sportchance_data:pd.DataFrame,
                        voivodeship: str = None,
                        age: int = None,
                        random_chance:bool = False)->pd.DataFrame:
        """Return sportstatus, one of {`None`, `"Junior"`, `"Senior"`}.
        Return depends mainly on sportchance_data, less on `age` and `voivodeship`
        or chance is drawn from `sportchance_data`.

        Args:
            `sportchance_data` (pd.DataFrame): df contains chance to get sportstatus 
                            depends on voivodeship and age.
            `voivodeship` (str, optional): One of `voivodeships` in Poland. 
                                        Required if `random_chance` = `False`.Defaults to None.
            `age` (int, optional): Age of person. Defaults to None.
            `random_chance` (bool, optional): If `True`, `age` and `voivodeship` have no effect
                                            to result. Defaults to False.

        Returns:
            Union[str, None]: Return str, if "Junior"|"Senior", else None.
        """
        
        # if random or no `age` or no `voivodeship` arg.
        if random_chance or age is None or voivodeship is None:
            return fast_choices([choice(["Junior", "Senior"]), None],
                                cls.sport_status_chance_by_data(
                                    sportchance_data,
                                    choice(sportchance_data.index),
                                    randint(0,100)))
            
        # out of accept age range
        elif age < 15 or age > 45:
            return None
        # junior
        elif 18> age>=15:
            return fast_choices(["Junior", None], 
                                cls.sport_status_chance_by_data(sportchance_data,
                                                                voivodeship,
                                                                age))
        # senior   
        elif age<39:
            return fast_choices(["Senior", None], 
                                cls.sport_status_chance_by_data(sportchance_data,
                                                                voivodeship,
                                                                age))
        # older senior
        elif age>=40:
            return fast_choices(["Senior", None], 
                                cls.sport_status_chance_by_data(sportchance_data,
                                                                voivodeship,
                                                                age)/2)
    
    @staticmethod
    def sport_status_chance_by_data(df: pd.DataFrame,
                                    voivodeship: str,
                                    age: int) -> float:
        """Return chance as float number to become a sportman in given voivodeship.
        Every voivodeship has diffrent total population and population involved in sports in diffrent age.

        Args:
            voivodeship (str): voivodeship 
            age (int): 
            df (pd.DataFrame): df contains chance to become a junior or senior in sport experience meaning.

        Returns:
            chance: chance to become a sportman in given voivodeship in given age.
        """
        if age < 15 or age > 45:
            return 0.
        elif age > 39 and age < 46:
            return df.at[voivodeship, "senior_chance"]/2
        elif age < 18 and age > 14:
            return df.at[voivodeship, "junior_chance"]
        return df.at[voivodeship, "senior_chance"]

if __name__ == '__main__':
    print(x := Athletes.generate_dataset(2,None,{"sportstatus":None}))
    