from collections import deque


class TimeRangeAverage:
    def __init__(self, time_range):
        self.__values = deque()
        self.__time_range = time_range

    def add_value(self, timestamp, value):
        self.__values.append((timestamp, value))
        time_limit = timestamp - self.__time_range
        while self.__values[0][0] < time_limit:
            self.__values.popleft()

    def reset(self):
        self.__values.clear()

    def average(self):
        if len(self.__values) == 0:
            return None

        print(f"LEN {len(self.__values)}")
        result = 0.0
        for _, value in self.__values:
            result += value
        return result / len(self.__values)
