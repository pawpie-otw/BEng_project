from pandas import DataFrame
from random import choices, choice
from typing import Union, Tuple, Any
from common_functions.custom_exceptions import IncorrectLen


def draw_from_df(*df_s: DataFrame, k: Union[int, Tuple[int]] = 1, equal_weight: bool = False) -> Union[Tuple[Any], Tuple[Tuple[Any]]]:
    
    """ This method draw values from given DFs considering the popular of name as weight.
    Args:
        df_s (DataFrame| List[DataFrame]): data to draw from.
        First col have to contains values and if equal_weights is False, second - weights.

        k (int | Tuple[int], optional): amount of return values 
        (if int: for every given df, if container of len equal to number of df_s: for each given df from df_s).
        Defaults to 1 (1 from each df).

        equal_weight (bool, optional): if True, every value has the same weight.
        Default to False.

    Returns:
        (Tuple[Any] | Tuple[Tuple[Any]]): Return Tuples of drawn values.


    Example of use:

        draw_from_df(df0, df1, k = 3) -> (
            (val0_from_df0, val1_from_df0, val2_from_df0),
            (val0_from_df1, val1_from_df1, val2_from_df1))

        draw_from_df(df0, df1, df2, k = [1,2,3]) -> (
            (val0_from_df0),
            (val0_from_df1, val1_from_df1),
            (val0_from_df2, val1_from_df2, val2_from_df2))
            
    """


    col_names = [df.columns for df in df_s]

    if isinstance(k, int):
        k = [k for _ in range(len(df_s))]
    elif not isinstance(k, (list, tuple)):
        raise TypeError("argument have to be int, tuple or list.")
    elif len(k) != len(df_s):
        raise IncorrectLen("Length of k should be equal to number of df_s.")

    if equal_weight:
        if any(i>1 for i in k):
            return tuple(choices(d_set[cols[0]], k=_k)
                         for d_set, cols,_k in zip(df_s, col_names, k))
    # else: return list
        else:
            return tuple(choice(d_set[cols[0]])
                         for d_set, cols in zip(df_s, col_names))
    # if k is greater then 1, then return tuple of tuples
    if any(i>1 for i in k):
        return tuple(choices(d_set[cols[0]], d_set[cols[1]], k=_k) 
                     for d_set, cols, _k in zip(df_s, col_names, k))
    # else: return list
    else:
        return tuple(choices(d_set[cols[0]], d_set[cols[1]])[0]
                     for d_set, cols  in zip(df_s, col_names))
