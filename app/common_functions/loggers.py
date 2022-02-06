from datetime import date, datetime
from pathlib import Path
from typing import Union
from functools import wraps
import time


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
            
def timeit_and_log(file_path, log_args=False, log_kwargs=False):
    def wrapper(func):
        @wraps(func)
        def ins_wrapper(*args, **kwargs):
            
            time_start = time.time()
            result = func(*args, **kwargs)
            time_stop = time.time()
            
            with open(file_path, "a") as f:
                
                now = datetime.now()
                f.write("\n")
                f.write("func name:"+str(func.__name__)+"\n")
                f.write("exe time:"+str(time_stop-time_start)+"\n")
                f.write("datetime:"+str(now.strftime("%Y-%m-%d %H:%M:%S"))+"\n")
                if log_args:
                    f.write("args:"+str(args)+"\n")
                if log_kwargs:
                    f.write("kwargs:"+str(kwargs)+"\n")
                
                f.write("\n")
                f.write("#"*50)
            return result
        return ins_wrapper
    return wrapper
    

def timeit_and_save(path=None):
    def timeit_wrapper(func):
        def wrapper(*args, **kwargs):
            start = time.time()    
            x = func(*args, **kwargs)
            stop = time.time()
            exe_time =start - stop
            if path is None:
                print(exe_time)
            else:
                with open(path, "a+") as f:
                    f.write(f"func name:      {func.__name__}")
                    f.write(f"execution time: {exe_time}")
            return x
        return wrapper
    return timeit_wrapper