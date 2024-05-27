from common_tools import *

# 输出开头和结尾提醒
def single_remind(start, end):
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            print_stack_trace(start+"……")
            res = func(*args, **kwargs)
            print_stack_trace(end+"！")
            return res
        return wrapper_func
    return decorator_func


# 重复多次
def repeat_operator(counter):
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            for i in range(counter):
                res = func(*args, **kwargs)
            return res
        return wrapper_func
    return decorator_func

def wait(counter):
    for i in range(counter):
        print_stack_trace(f"休眠中：{counter-i}s/{counter}s")
        sleep(1)
    print_stack_trace(f"休眠完成")

def TODO(func):
    def wrapper():
        print_stack_trace("还未完成："+str(func))
        return func
    return wrapper()


def nothing():
    return None
