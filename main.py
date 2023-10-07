import locale
from datetime import datetime
# pymorphy2 работает на python 3.11 с ошибками
import pymorphy3
import calendar as calendar_module


class Calendar:
    def __init__(self):
        self.calendar_days = {}
        self.months = [i for i in calendar_module.month_name[1:]]

        self.make_calendar_days()

    def __iter__(self):
        return self.CalendarIterator(self)

    def make_calendar_days(self):
        current_year = datetime.now().year

        for i, month in enumerate(self.months):
            self.calendar_days[month] = calendar_module.monthrange(current_year, i + 1)[1]

    class CalendarIterator:
        def __init__(self, calendar):
            self.__calendar = calendar
            self.__index = 0
            self.__calendar_iterable = []
            self.__make_iterable_calendar()

        def __iter__(self):
            return self

        def __next__(self):
            if self.__index >= len(self.__calendar_iterable):
                raise StopIteration

            day = self.__calendar_iterable[self.__index]
            self.__index += 1

            return day

        def __make_iterable_calendar(self):
            morph = pymorphy3.MorphAnalyzer()
            for k, v in self.__calendar.calendar_days.items():
                month = morph.parse(k.lower())[0].inflect({'gent'}).word
                self.__calendar_iterable.extend(
                    [f'{i} {month}' for i in range(1, v + 1)]
                )


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

if __name__ == '__main__':
    c = Calendar()

    # 1 вариант проверки
    # print(c.calendar_days)
    # for day in c:
    #     print(day)

    # 2 вариант проверки
    c_iter = iter(c)
    while True:
        print(next(c_iter))