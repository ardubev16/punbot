#!/usr/bin/env python3


def average(values):
    length = len(values)
    return sum(values) / length


def icon(value: float):
    if value > 0:
        return "📈"
    elif value < 0:
        return "📉"
    else:
        return "🔷"
