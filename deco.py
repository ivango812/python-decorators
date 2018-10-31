#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import update_wrapper, wraps, reduce


def disable(func):
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def decorator(func):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper


def countcalls(func):
    '''Decorator that counts calls made to the function decorated.'''

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        wrapper.calls += 1
        return result

    wrapper.calls = 0
    return wrapper


def memo(func):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):

        h = hash(args)
        if h not in wrapper.cache:
            wrapper.cache[h] = func(*args, **kwargs)

        result = wrapper.cache[h]

        return result

    wrapper.cache = {}
    return wrapper


def n_ary_func(function, sequence):
    if len(sequence) == 1:
        return sequence[0]
    elif len(sequence) >= 2:
        return function(sequence[0], n_ary_func(function, sequence[1:]))
    else:
        raise TypeError("%s() of empty sequence" % function.__name__)


def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''

    @wraps(func)
    def wrapper(*args):
        return n_ary_func(func, args)

    return wrapper


def trace(indent):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''
    def real_decorator(func):

        real_decorator.depth = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(indent * real_decorator.depth, '-->', '%s(%s)' % (func.__name__, *args))
            real_decorator.depth += 1
            result = func(*args, **kwargs)
            real_decorator.depth -= 1
            print(indent * real_decorator.depth, '<--', '%s(%s) == ' % (func.__name__, *args),
                  result)
            return result

        return wrapper

    return real_decorator


# memo = disable
@countcalls
@memo
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


# @decorator
@countcalls
@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    # return
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    print('__doc__=', fib.__doc__)
    fib(3)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
