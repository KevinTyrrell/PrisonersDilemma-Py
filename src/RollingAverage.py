"""
Simulates and attempts to solve the prisoner's dilemma using a genetic algorithm.
    Copyright (C) 2021  Kevin Tyrrell

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class RollingAverage:
    """
    Constructs a new rolling average.

    @:param value: Optional value to initialize the average with.
    """
    def __init__(self, value: float = None):
        self.next = self.__next_init
        if value is not None:
            self.__next_init(value)

    """
    @:return average: Current state of the rolling average.
    """
    @property
    def average(self) -> float:
        return self.__avg

    """
    Initializes the rolling average with a value.
    To be used with the delegation design pattern.
    
    @:param value: 
    """
    def __next_init(self, value: float) -> float:
        self.__count = 1
        self.__avg = value
        self.next = self.__next
        return value

    """
    Calculate the next step of the rolling average.

    @:param value: Value to add to the rolling average.
    @:return: Current average, including the specified value.
    """
    def __next(self, value: float) -> float:
        self.__count += 1
        self.__avg += (value - self.__avg) / self.__count
        return self.__avg
