#!/usr/bin/env python3


def average(values):
    length = len(values)
    return sum(values) / length


def icon(new_value: float, avg: float):
    diff = new_value - avg
    if diff > 0:
        return "📈"
    elif diff < 0:
        return "📉"
    else:
        return "🔷"
