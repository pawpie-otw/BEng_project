from datetime import date, datetime
from pathlib import Path
from typing import Union
from functools import wraps
from time import time_ns


def log_to_file(filename:Union[Path, str], **kwargs)->None:
    """Log to file every param given as kwarg with current date and time.

    Args:
        `filename` (Union[Path, str]): path to file to save logs
        `**kwargs` (Any): arguments to store in file as logs.
    """
    today = date.today()
    now = datetime.now()
    
    with open(filename, "a") as file:
        file.write("date:",today.strftime("%d/%m/%Y"))
        file.write("time:",now.strftime("%H:%M:%S"))
        for kwarg in kwargs:
            file.write("arg_name:",kwarg)
            file.write("value   :",kwargs[kwarg])
        file.write(f"\n{'#'*50}\n")
            
def timeit_and_log(file_path):
    def wrapper(func):
        @wraps(func)
        def ins_wrapper(*args, **kwargs):
            
            time_start = time_ns()
            result = func(*args, **kwargs)
            time_stop = time_ns()
            
            with open(file_path, "a") as f:
                
                now = datetime.now()
                f.write("datetime:"+str(now.strftime("%Y-%m-%d %H:%M:%S")))
                f.write("func name:"+str(func.__name__))
                f.write("args:"+str(args))
                f.write("kwargs:"+str(kwargs))
                f.write("exe time:"+str(time_stop-time_start))
                f.write("#"*50)
            return result
        return ins_wrapper
    return wrapper
    

