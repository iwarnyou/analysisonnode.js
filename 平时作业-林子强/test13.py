#!/usr/bin/env python
# coding: utf-8

from sys import settrace

def tracer(frame, event, arg):
    func_name = frame.f_code.co_name
    line_no = frame.f_lineno
    f_locals = frame.f_locals
    print(f"event: {event}, function: {func_name}, lineno: {line_no}, locals: {f_locals}")
    return tracer

def foo(bar):
    buz = bar + 1
    bar *= buz
    if bar > buz:
        bar -= buz
    return bar + buz

old_tracer = settrace(tracer)
foo(10)
settrace(old_tracer)
