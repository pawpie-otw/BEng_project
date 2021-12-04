from pandas import DataFrame
from random import choices
from typing import Union, Tuple, Any


def draw_from_df(*df_s: DataFrame, k: Union[int, Tuple[int]] = 1, equal_weight: bool = False) \
        -> Union[Tuple[Any], Tuple[Tuple[Any]]]:
    """This method draw values from given DFs considering the popular of name as weight.

    Args:
        df_s (DataFrame| List[DataFrame]): data to draw from.
        First cols have to contain values, second - weights.

        k (int | Tuple[int], optional): amount of return values 
        (if int: for every given df, if container: for each given df).
        Defaults to 1 (1 from each df).

        equal_weight (bool, optional): if True, every value has the same weight.
        Default to False.

    Returns:
        Tuple[Any] | Tuple[Tuple]: Return Tuples of drawn values.
    """
    col_names = [df.columns for df in df_s]

    # if k is greater then 1, then return list of lists
    if k > 1:
        return tuple(tuple(choices(d_set[cols[0]], d_set[cols[1]], k=k))
                     for d_set, cols in zip(df_s, col_names))
    # else: return list
    else:
        return tuple(choices(d_set[cols[0]], d_set[cols[1]])[0]
                     for d_set, cols in zip(df_s, col_names))
