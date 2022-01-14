from typing import Sequence, Any


class PredefinedTypes:
    
    @classmethod
    def dict_checkbox(cls,
                    name:str,
                    repr_:str,
                    desc:str,
                    checked:bool=False)->dict:

        return cls.base_dict(name,repr_,desc).update(
                                {
                                "input_type": "checkbox",
                                "return_type": "bool",
                                "checked":checked,
                                }
                            )
    
    @classmethod
    def dict_range(cls,
                name:str,
                repr_:str,
                desc:str,
                min_:int=0,
                max_:int=100,
                default:int=0,
                step:int=1)->dict:
        return cls.base_dict(name,repr_,desc).update(
                                {
                                "input_type": "range",
                                "return_type": "int",
                                "min":min_,
                                "max":max_,
                                "default":default,
                                "step":step
                                }
                            )
    @classmethod
    def dict_text(cls,
                name:str,
                repr_:str,
                desc:str,
                maxlength:int=20)->dict:
        return cls.base_dict(name, repr_ ,desc).update(
                                {
                                    "input_type":"text",
                                    "return_type":"str",
                                    "maxlength": maxlength
                                }
                            )
    @classmethod
    def custom_col_name(cls)->dict:
        """
        Returns:
            dict: Dict for custom column name.
        """
        return cls.dict_text("cust_col_name",
                             "Własna nazwa",
                             "Własna nazwa kolumny.")
    @classmethod
    def blanck_chance(cls)->dict:
        """
        Returns:
            dict: dict for blank chance.
        """
        return cls.dict_range("blank_chance",
                              "Szansa na brak wartości",
                              "Szansa na brak wartości przedstawiona w postaci procent.")
        
    @classmethod
    def dict_select(cls,
                    name:str,
                    repr_:str,
                    desc:str,
                    options:Sequence[str])->dict:
        
        return cls.base_dict(name, repr_, desc).update(
                                {
                                    "options":options
                                }
                            )
    @classmethod
    def dict_number(cls,
                name:str,
                repr_:str,
                desc:str,
                min_:int=0,
                max_:int=100,
                default:int=0,
                step:int=1)->dict:
        return cls.base_dict(name,repr_,desc).update(
                                {
                                "input_type": "number",
                                "return_type": "int",
                                "min":min_,
                                "max":max_,
                                "default":default,
                                "step":step
                                }
                            )
    @staticmethod
    def dict_option(repr_:str,
                    value:Any)->dict:
        return {
            "repr": repr_,
            "value":value}
    
    @staticmethod
    def base_dict(name:str,
                repr_:str,
                desc:str)->dict:
        
        return {"name": name,
                "repr": repr_,
                "description": desc}