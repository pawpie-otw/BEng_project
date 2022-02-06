from http.client import ResponseNotReady
from typing import Sequence, Any


class PredefinedTypes:

    @classmethod
    def dict_checkbox(cls,
                      name: str,
                      repr_: str,
                      desc: str,
                      default: bool = False,
                      checked: bool = False) -> dict:

        response = cls.base_dict(name, repr_, desc)
        response.update(
            {
                "input_type": "checkbox",
                "return_type": "bool",
                "default": default,
                "checked": checked,
            }
        )
        return response

    @classmethod
    def dict_range(cls,
                   name: str,
                   repr_: str,
                   desc: str,
                   min_: int = 0,
                   max_: int = 100,
                   default: int = 0,
                   step: int = 1) -> dict:
        response = cls.base_dict(name, repr_, desc)
        response.update(
            {
                "input_type": "range",
                "return_type": "int",
                "min": min_,
                "max": max_,
                "default": default,
                "step": step
            }
        )
        return response

    @classmethod
    def dict_text(cls,
                  name: str,
                  repr_: str,
                  desc: str,
                  maxlength: int = 20) -> dict:
        response = cls.base_dict(name, repr_, desc)
        response.update(
            {
                "input_type": "text",
                "return_type": "str",
                "maxlength": maxlength
            }
        )
        return response

    @classmethod
    def custom_col_name(cls) -> dict:
        """
        Returns:
            dict: Dict for custom column name.
        """
        return cls.dict_text("cust_col_name",
                             "Własna nazwa",
                             "Własna nazwa kolumny.")

    @classmethod
    def blanck_chance(cls) -> dict:
        """
        Returns:
            dict: dict for blank chance.
        """
        return cls.dict_range("blanck_chance",
                              "Szansa na brak wartości",
                              "Szansa na brak wartości przedstawiona w postaci procent.")

    @classmethod
    def dict_select(cls,
                    name: str,
                    repr_: str,
                    desc: str,
                    options: Sequence[str]) -> dict:

        response = cls.base_dict(name, repr_, desc)
        response.update(
            {
                "default": options[0]["value"],
                "options": options
            }
        )
        return response

    @classmethod
    def dict_number(cls,
                    name: str,
                    repr_: str,
                    desc: str,
                    min_: int = 0,
                    max_: int = 100,
                    default: int = 0,
                    step: int = 1) -> dict:
        response = cls.base_dict(name, repr_, desc)
        response.update(
            {
                "input_type": "number",
                "return_type": "int",
                "min": min_,
                "max": max_,
                "default": default,
                "step": step
            }
        )
        return response

    @staticmethod
    def dict_option(repr_: str,
                    value: Any) -> dict:
        return {
            "repr": repr_,
            "value": value}

    @staticmethod
    def base_dict(name: str,
                  repr_: str,
                  desc: str) -> dict:

        return {"name": name,
                "repr": repr_,
                "description": desc}
