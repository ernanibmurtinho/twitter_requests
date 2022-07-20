"""
Function decorator.

This module provides a function decorator that can be used to wrap a function
"""
from twitter_ingestion.utils.decorators import TimerDecorator

timerDecorator = TimerDecorator()
timer = timerDecorator.timer

__all__ = [
    'twitter',
    'timer'
]

__version__ = '1.0.0'
