def log_to_file_if_exception_raised(file_path):
    """Log data to file when exception is raised.
    Data:
    - function name,
    - args,
    - kwargs,
    - error message.
    """
    def wrapper(func_name):
        def inner_wrapper(*args, **kwargs):
            try:
                return func_name(*args, **kwargs)
            
            except Exception as e:
                with open(file_path, "a") as f:
                    f.write(f"""\n\nFunction: {func_name.__name__},
                            args: {args},
                            kwargs: {kwargs},
                            exception: {e}:{str(e)}""")
                return "bad_field"
        return inner_wrapper
    return  wrapper