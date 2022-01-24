from typing import Dict, Any, List, Union
from urllib import response

from field_types import AVAILABLE_FIELDS
from dependencies import DEPENDENCIES


class FieldInterpreter:
    def __init__(self, available_fields: List[Dict[str, Union[str, Dict[str, Any]]]], dependencies) -> None:
        """
        Args:
            available_fields (List[Dict[str, Union[str, Dict[str, Any]]]])
            This arg must contain available field in the schema.
        """
        self.available_fields = available_fields
        self.dependencies = dependencies

    def check_requested_cols_for_dependencies(self, requested_fields):
        response = set()
        for field, options in requested_fields.items():
            response = response.union(
                self.if_need_dependencies(field, options))
        return response

    def if_need_dependencies(self, field_name: str, options) -> set:
        """ check if current field with current options need other field.
        Return set of required columns.
        Args:
            field_name ([type]): [description]
            options ([type]): [description]

        Returns:
            set: set of required fields. Empty, if this field no need other one.
        """
        curr_field_dep = self.dependencies[field_name]
        response = set()
        for condition, required_cols in curr_field_dep.items():
            if not options[condition]:
                response = response.union(required_cols)
        return response

    def fix_request(self, requested_data, clean=True, fill=True):
        if clean and fill:
            return {field_name: self.clean_and_refill(field_name, options)
                    for field_name, options in requested_data.items()}

        elif clean:
            return {field_name: self.clean_field(field_name, requested_data[field_name])
                    for field_name in requested_data}

        elif fill:
            return {field_name: self.fill_field(field_name, requested_data[field_name])
                    for field_name in requested_data}

    def clean_and_refill(self, name, current_params):
        clear = self.clean_field(name, current_params)
        refilled = self.refill_field(name, clear)
        return refilled

    def clean_field(self, name, current_params) -> Dict[str, Any]:

        default_set = self.get_default_options_for(name)
        return {option: value
                for option, value in current_params.items()
                if option in default_set}

    def refill_field(self, name: str, current_params: Dict[str, Any] = {}) -> Dict[str, Any]:

        param_copy = {key: val
                      for key, val in current_params.items()}

        missing = self.return_missing_options(name, current_params)
        param_copy.update(missing)

        return param_copy

    def return_missing_options(self, name: str,
                               current_params: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Looking for missing params for given field name

        Args:
            name (str): name of field you want to check for misiing params
            current_params (Dict[str, Any]): current params

        Returns:
            Dict[str, Any]: return dict with missing params.
        """
        default_set = self.get_default_options_for(name)

        return {option: default_set[option]
                for option in default_set
                if not option in current_params}

    def get_default_options_for(self, name):
        field = self.get_default_field(name)

        response = {"custom_col_name": None}

        for option in field["options"]:
            response[option["name"]] = option["default"]

        return response

    def get_default_field(self, name) -> dict:
        for field in self.available_fields:
            if field["name"] == name:
                return field
        raise KeyError("No field in available field list")


if __name__ == '__main__':
    fi = FieldInterpreter(AVAILABLE_FIELDS, DEPENDENCIES)
    repaired_cols = fi.fix_request({"voivodeship": {
                                                "custom_col_ame": "Wojewodztwo",
                                                "equal_weight": False,
                                                "blanck_chance": 50},
                                "sportdiscipline": {
                                                "custom_col_name": "dyscyplina",
                                                "equal_weight": False,
                                                "blanck_chance": 0
                                                }
                                })  

    required_cols = fi.check_requested_cols_for_dependencies(repaired_cols)
    print(required_cols)
