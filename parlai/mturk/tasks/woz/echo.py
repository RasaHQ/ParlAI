
import functools
from typing import Text, Optional, Callable, Dict, Any
from datetime import datetime
import inspect
import os


def identity(arg: Any) -> Any:
    return arg


def log_write(message: Text) -> None:
    with open(os.path.expanduser("~/RASA-ParlAI.log"), "a+") as file:
        time = str(datetime.now().isoformat())
        file.write(f"{time}\t{message}\n")


def echo_out(prefix: Optional[Text] = None, epilog: Optional[Callable] = None, output: Callable[[Text], None] = print):
    _prefix = prefix or ""

    def echo_wrapper(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if epilog:
                output(f"{_prefix}{epilog(result)}")
            else:
                output(f"{_prefix}{result}")
            return result
        return wrapper
    return echo_wrapper


def echo_in(prefix: Optional[Text] = None, prolog: Optional[Dict[Text, Callable]] = None, output: Callable[[Text], None] = print):
    _prefix = prefix or ""

    def echo_wrapper(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            arg_names = list(inspect.signature(function).parameters.keys())
            defaults = function.__defaults__
            all_args = dict(zip(arg_names[:len(args)], args))
            if defaults:
                all_args.update(dict(zip(arg_names[len(args):], defaults)))

            _prolog = {}
            for arg, f in prolog.items():
                _prolog[arg] = f or identity

            if prolog and all_args:
                args_text = args_to_text(**{arg: f(all_args[arg]) for arg, f in _prolog.items()})
            else:
                args_text = args_to_text(*args, **kwargs)
            output(f"{_prefix}{function.__name__}({args_text})")
            return result
        return wrapper
    return echo_wrapper


def echo(prefix: Optional[Text] = None, epilog: Optional[Callable] = None, output: Callable[[Text], None] = print):
    _prefix = prefix or ""

    def echo_wrapper(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            args_text = args_to_text(*args, **kwargs)
            if epilog:
                output(f"{_prefix}{function.__name__}({args_text}) ~ {epilog(result)}")
            else:
                output(f"{_prefix}{function.__name__}({args_text}) = {result}")
            return result
        return wrapper
    return echo_wrapper


def args_to_text(*args, **kwargs) -> Text:
    args_texts = []
    for item in args:
        args_texts.append(f"{item}")
    kwargs_texts = []
    for key, value in kwargs.items():
        kwargs_texts.append(f"{key}={value}")

    if args_texts and kwargs_texts:
        return ", ".join(args_texts) + ", " + ", ".join(kwargs_texts)
    elif args_texts:
        return ", ".join(args_texts)
    elif kwargs_texts:
        return ", ".join(kwargs_texts)
    else:
        return ""


def unpack_args(function: Callable) -> Dict[Text, Any]:
    # code = function.__code__
    # argcount = code.co_argcount
    # argnames = code.co_varnames[:argcount]
    # fn_defaults = function.__defaults__ or list()
    # return dict(zip(argnames[-len(fn_defaults):], fn_defaults))
    # return dict(signature(function).bind(0, 0).apply_defaults())
    return {name: p.default for name, p in inspect.signature(function).parameters.items()}


if __name__ == '__main__':
    @echo_in(prefix="j: ", prolog={"a": lambda x: x + 1, "p": lambda x: x})
    def foo(a, b, p=3):
        return a + b + p

    print(foo(2, 7))
    print()
    print(list(inspect.signature(foo).parameters.keys()))
