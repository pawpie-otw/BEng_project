def wrapper(func):
    def ins_wrapper(*args, **kwargs):
        # tu cialo dekoratora
        result = func(*args, **kwargs)
        # tu cialo dekoratora
        return result
    return ins_wrapper

wrapper(print)("aaaa", "bbb")

@wrapper
def my_print(*args)->None:
    print(*args)


def out_wrapper(wrapper_arg):
    def wrapper(func):
        def ins_wrapper(*args, **kwargs):
            # tu cialo dekoratora
            result = func(*args, **kwargs)
            # tu cialo dekoratora
            return result
        return ins_wrapper
    return wrapper

@out_wrapper(2)
def my_print2(*args)->None:
    print(*args)

out_wrapper(2)(print)("aaaa", "bbb")