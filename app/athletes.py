import pandas as pd

from typing import Union, Dict, Any
from random import choice, randint

from common_functions.extra_funcs import fast_choices

from data.athletes.sports_data import Data




class Athletes:

    '''Class for generating athletes dataset'''

    path_dict = {
        "sportstatus":r"data/athletes/sportstatus_chance.csv"
    }
    
    data = Data()

    

    @classmethod
    def generate_dataset(cls,
                         rows: Union[None,int],
                         base_df: Union[None, pd.DataFrame] = None,
                         sportstatus:Union[None, Dict[str, Any]] = None,
                         sportdyscipline:Union[None, Dict[str, Any]] = None) -> Dict[str, pd.Series]:
        
        sportstatus_data = pd.read_csv(cls.path_dict["sportstatus"], index_col='voivodeship')
        
        result = {}
        
        # if sport status 
        if sportstatus:
            # but completely random
            if sportstatus.get("random_chance") or base_df is None:
                result["sportstatus"] = pd.Series([cls.generate_sportstatus(sportstatus_data, random_chance=True)
                                                       for _ in range(rows)])
            # 2 params
            elif all(["age" in base_df.columns, "voivodeship" in base_df.columns]):
                result["sportstatus"] = base_df.apply(lambda x: cls.generate_sportstatus(sportstatus_data,
                                                                                    voivodship=x.voivodeship,
                                                                                    age=x.age))
            elif "age" in base_df.columns:
                result["sportstatus"] = base_df.apply(lambda x: cls.generate_sportstatus(sportstatus_data,
                                                                                    voivodship=choice(sportstatus_data.index),
                                                                                    age=x.age))
            elif "voivodeship" in base_df.columns:
                result["sportstatus"] = base_df.apply(lambda x: cls.generate_sportstatus(sportstatus_data,
                                                                                    voivodship=x.voivodeship,
                                                                                    age=randint(0,100)))
        
        return result
      
        # elif sportstatus and isinstance(base_df, dict):
            
        #     # verify data
            
        #     # if base_df is DF and has requirements to generate dependence data.
        #     if condition? :
                
        #         if all(["voivodeship" in base_df.keys(), "age" in base_df.keys()]):
        #             result["sportstatus"] =  pd.Series([cls.generate_sportstatus(sportstatus_data, voivodeship, age)
        #                                                for voivodeship, age in zip(base_df["voivodeship"], base_df["age"])])
        #         # if data is incomplete
        #         else :
                    
                    
                                                           
        #             result["sportstatus"] = pd.Series([cls.generate_sportstatus(sportstatus_data, voivodeship, age)
        #                                                for voivodeship, age in zip(base_df["voivodeship"], base_df["age"])])
            
        #     # if "completely" random 
            
        # if sport_params:
        #     pass        
        #     # result["sports_discipline"] = pd.Series([draw_from_df(__class__.create_provinces_dict()[voivodship])
            #                   for voivodship in base_df.voivodship])
        

    @classmethod
    def create_provinces_dict(cls):
        all_sports = cls.data.join_all_sports()
        all_to_dict = all_sports.drop(columns=["Nazwa"])
        sport_names = []
        for col in all_to_dict.columns:
            sport_names.append(col)
        sport_names_series = pd.Series(sport_names)
        dfs_provinces_dict = {}
        for index, row in all_sports.iterrows():
            dfs_provinces_dict[row[0]] = pd.DataFrame(
                {'Name': sport_names_series, 'People': row[1:].reset_index(drop=True)})

        return dfs_provinces_dict
    
    @classmethod
    def generate_sportstatus(cls,
                        sportchance_data:pd.DataFrame,
                        voivodeship: str = None,
                        age: int = None,
                        random_chance:bool = False)->Union[str, None]:
        """Return sportstatus, one of {`None`, `"Junior"`, `"Senior"`}.
        Return depends mainly on sportchance_data, less on `age` and `voivodeship`
        or chance is drawn from `sportchance_data`.

        Args:
            `sportchance_data` (pd.DataFrame): df contains chance to get sportstatus 
                            depends on voivodeship and age.
            `voivodship` (str, optional): One of `voivodeships` in Poland. 
                                        Required if `random_chance` = `False`.Defaults to None.
            `age` (int, optional): Age of person. Defaults to None.
            `random_chance` (bool, optional): If `True`, `age` and `voivodeship` have no effect
                                            to result. Defaults to False.

        Returns:
            Union[str, None]: Return str, if "Junior"|"Senior", else None.
        """
        
        # if random or no `age` or no `voivodeship` arg.
        if random_chance or age is None or voivodeship is None:
            print(sportchance_data.columns)
            return fast_choices([choice(["Junior", "Senior"]), None],
                                cls.sport_status_chance_by_data(
                                    sportchance_data,
                                    choice(sportchance_data.columns),
                                    randint(0,100))
                                )
            
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
        print("\n"*4)
        print(voivodeship, age)
        if 15 > age or age > 45:
            return 0
        elif 39 < age < 46:
            return df.loc[voivodeship, "senior_chance"]/2
        elif 18 > age > 14:
            return df.loc[voivodeship, "junior_chance"]
        return df.loc[voivodeship, "senior_chance"]