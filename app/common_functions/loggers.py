from datetime import date, datetime
from pathlib import Path
from typing import Union
from functools import wraps
import time

from nbformat import write


def log_to_file(filename:Union[Path, str], *args, **kwargs):
    """Log to file every param given as kwarg with current date and time.

    Args:
        `filename` (Union[Path, str]): path to file to save logs
        `**kwargs` (Any): arguments to store in file as logs.
    """
    today = date.today()
    now = datetime.now()
    
    with open(filename, "a") as file:
        file.write("date: ",today.strftime("%d/%m/%Y"))
        file.write("time: ",now.strftime("%H:%M:%S"))
        file.write("; ".join(args))
        for kwarg, value in kwargs.items():
            file.write(f"{kwarg}= {value};")
        file.write(f"\n")
            
def timeit_and_log(file_path, rows=None, log_args=False, log_kwargs=False):
    def wrapper(func):
        @wraps(func)
        def ins_wrapper(*args, **kwargs):
            
            time_start = time.time()
            result = func(*args, **kwargs)
            time_stop = time.time()
            
            with open(file_path, "a") as f:
                
                now = datetime.now()
                f.write("\n")
                f.write("func name: "+str(func.__name__)+"\n")
                if rows:
                    f.write("rows number: "+str(rows))
                f.write("exe time: "+str(time_stop-time_start)+"\n")
                f.write("datetime: "+str(now.strftime("%Y-%m-%d %H:%M:%S"))+"\n")
                if log_args:
                    f.write("args: "+str(args)+"\n")
                if log_kwargs:
                    f.write("kwargs: "+str(kwargs)+"\n")
                
                f.write("\n")
                f.write("#"*50)
            return result
        return ins_wrapper
    return wrapper