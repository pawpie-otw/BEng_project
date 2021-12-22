from __future__ import annotations
import random as rd
import sys
import numpy as np
from typing import Optional, List
from collections import defaultdict


def custom_number(min_val: int = -sys.maxsize - 1,
                  max_val: int = sys.maxsize,
                  range_chance: List[int] = [100],
                  round_: int = None) -> float:
    """ Draw a number from given range. Allow also to divide a range to equal subranges and assign a chance to each of them.
    Args:
        min_val (int, optional): lowest lim of number range. Defaults min allowed number.
        max_val (int, optional): max lim of number range. Defaults to max allowed number.
        range_chance (List[int], optional): divide a range to n:=len(change_chance) subranges and give then a chance to be drawn. 
        Defaults to [100] - the same chance for every number in all given range.
        round_ (int, optional): round a returned value to passed decimals as parameter. Defaults to None (not round).

    Returns:
        float: drawn value, optionally rounded
    """
    n: int = len(range_chance)
    # create a borders
    comp_div: np.array = np.linspace(min_val, max_val, n+1)

    # choose a range
    a = rd.choices(range(n), range_chance, k=1)[0]

    # draw and optionally round
    if round_:
        round(rd.uniform(comp_div[a], comp_div[a+1]), round_)
    return rd.uniform(comp_div[a], comp_div[a+1])


if __name__ == '__main__':
    pass
