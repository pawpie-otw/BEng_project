import collections

from random import choices, randint
from typing import Union, Any, Callable, Annotated, Sequence

from common_functions.log_wrapper import log_to_file_if_exception_raised

@log_to_file_if_exception_raised("/extra_funcs.errors")
def if_not_then_none(expression:Any, method_to_check:Callable=None, *args, **kwargs)->Union[None,Any]:
    """Universal method to test expression. If condition return false, then return None.

    Args:
        `expression` (Any): Any object to verify.
        `method_to_check` (Callable, optional): if given, will be used as condition method.
        *args | **kwargs: will be pass to `method_to_check` function.
    Returns:
        Union[None,Any]: None if the condition is not met, else `expression`.
    """
    if method_to_check is not None:
        if method_to_check(expression, *args, **kwargs):
            return expression
        
    elif expression:
        return expression
    return None

@log_to_file_if_exception_raised("/extra_funcs.errors")
def concatenate_strings(expression:Union[str, Sequence[str]], 
                          sep: Annotated[str, 1]=" ")->str:
        """Concatenate given sequence of string into one string separated by sep: char.

        Args:
            expression (Union[str, Sequence[str]]): String(s) to cancatenate.
            sep (Annotated[str, 1], optional): Separator dividing strings after concatenad.
                                                Defaults to " ".

        Returns:
            str: Concatenated strings.
        """
        
        if isinstance(expression, collections.Sequence):
            return sep.join(expression)
            
        elif isinstance(expression, str):
            return expression
        
def fast_choices(population: Annotated[Sequence[Any],2],
                 chance_for_first: Union[int, float])->Any:
    """Pre-prepared random.choices for the project.

    Args:
        population (Annotated[Sequence[Any],2]): Population like in choice/choices, but len =2.
        chance_for_first (Union[int, float]): percente chance for first element.

    Returns:
        Any: 1 of 2 element given as population.
    """
    return choices(population, (100-chance_for_first, chance_for_first))[0]

def insert_value(list_:Sequence[Any], chance_:int, value_:Any=None)->Sequence[Any]:
    return [v
        if randint(0,100)<=chance_
        else value_
        for v in list_]