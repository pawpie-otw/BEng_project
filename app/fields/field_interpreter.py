from typing import Dict, Any, List, Union

from response.response_types import RESPONSES
from fields.predefined_types import PredefinedTypes as PT

from common_functions import loggers

class FieldInterpreter:
    def __init__(self, available_fields: List[Dict[str, Union[str, Dict[str, Any]]]], dependencies) -> None:
        """
        Args:
            available_fields (List[Dict[str, Union[str, Dict[str, Any]]]])
            This arg must contain available field in the schema.
        """
        self.available_fields = available_fields
        self.dependencies = dependencies
        
    @loggers.timeit_and_log("./logs/interprete.logs")
    def validate_request(self, request_data):
        
        if {"fields","general"} != set(request_data.keys()):
            raise KeyError("No required data: `fields` or `general`.")
        
        elif type(request_data["fields"])!=dict or len(request_data["fields"].keys())<1:
            raise ValueError("[`fields`] must containt at least one key!")
        
        else:
            for value in request_data["fields"].values():
                if type(value)!=dict:
                    raise TypeError("Every value in [`fields`] must be at least an empty dict.")
        
        try:
            int(request_data["general"].get("rows"))
        except Exception as e:
            raise ValueError("Request requires int value under ['general']['rows'].")
        
        if not request_data["general"].get("response_format") in [x[1] for x in RESPONSES]:
            raise ValueError("Correct response format are required.")
        
        for field, options in request_data["fields"].items():
            self.valid_field(field, options)
            
    @loggers.timeit_and_log("./logs/interprete.logs")
    def check_requested_cols_for_dependencies(self, requested_fields):
        response = set()
        for field, options in requested_fields.items():
            response = response.union(
                self.if_need_dependencies(field, options))
        return response - set(requested_fields.keys())

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
                for res in response:
                    response = response.union(self.if_need_dependencies(
                        res, self.get_default_options_for(res)))
        return response
    
    @loggers.timeit_and_log("./logs/interprete.logs")
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
        print(name)
        clear = self.clean_field(name, current_params)
        refilled = self.refill_field(name, clear)
        return refilled

    def clean_field(self, name, current_params) -> Dict[str, Any]:

        default_set = self.get_default_options_for(name)
        return {option: value
                for option, value in current_params.items()
                if option in default_set}

    def refill_multiple_fields(self, names_set) -> dict:
        return {name: self.get_default_options_for(name)
                for name in names_set}

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
        raise KeyError(f"No `{name}` field in available field list")


    def valid_field(self, field_name, options:Dict[str, Any]):
        
        for requested_option, requested_value in options.items(): # wszystkie nazwy/klucze zadanych opcji
            option_params = self.find_option_by_name(requested_option, field_name)
            
            x = {"checkbox":self.valid_checkbox,
            "range":self.valid_range,
            "text":self.valid_text
            }[option_params["input_type"]](requested_value, option_params)
                
    def find_option_by_name(self, option_name:str, field_name:str=None, search_all=False)->dict:
        """Return option data if option is available, else raise KeyError.

        Args:
            option_name (str): 
            field_name (str):
            search_all (bool): if True, looking for option in every field field_name is not required.
            

        Raises:
            KeyError: [description]

        Returns:
            dict[str, Any]
        """
        default_field_data = self.get_default_field(field_name)
        
        if option_name == "custom_col_name":
            return PT.custom_col_name()
        
        for av_option in default_field_data["options"]:
            if option_name == av_option["name"]:
                return av_option
        else:
            raise KeyError(f"No {option_name} in available {field_name} options.")
    
    
    
    
    def valid_text(self, curr_value, option_params):
        
        if len(str(curr_value))> option_params["maxlength"]:
            raise ValueError(f"{option_params} option too length! Max available option: {option_params['maxlength']}.")
        return True
    
    def valid_range(self, curr_value, option_params):
        
        if type(option_params["max"])==type(option_params["step"]):
            if type(option_params["max"]) == int and curr_value%1!=0:
                raise TypeError(f"{option_params['name']} is wrong type! Value must be an int!")
            
        elif not type(curr_value) in {float, int}:
            raise TypeError(f"{option_params} option must be a number!")
                
        available_value = range(option_params["min"], option_params["max"]+1, option_params["step"])
        
        if not curr_value in available_value:
            raise ValueError(f"Value {curr_value} not in available value {available_value}.")
        
        return True 
        
    
    def valid_checkbox(self, curr_value, option_params=None):
        if isinstance(curr_value, bool):
            return True
        else:
            raise TypeError(f"Value type must be a `bool`, not {type(curr_value)}")
        
        
