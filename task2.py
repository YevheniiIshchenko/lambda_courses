# 1 - rus, 2 - ukr, 3 -eng
from datetime import datetime, timedelta


class Document(object):

    base_filetypes = ['doc', 'docx', 'rtf']

    lang = {
        'Rus': 1,
        'Ukr': 2,
        'Eng': 3,
    }

    min_prices = {
        1: 50,
        2: 50,
        3: 120
    }

    price_sym = {
        1: 0.05,
        2: 0.05,
        3: 0.12,
    }

    speed = {
        1: 1333/60,
        2: 1333/60,
        3: 333/60,
    }

    start_hours = 10
    end_hours = 19
    start_day = 0
    end_day = 4

    def __init__(self, filetype: str, num_sym: int, lang: int):
        self.filetype = filetype
        self.num_sym = num_sym
        self.lang = lang

    def calculate_price(self) -> float:
        price = self.num_sym * self.price_sym[self.lang]
        # print(price)
        if self.filetype not in self.base_filetypes:
            price *= 1.2
        if price < self.min_prices[self.lang]:
            price = self.min_prices[self.lang]
        return price

    def calculate_time(self) -> float:
        min_time = 60
        time = 30 + self.num_sym/self.speed[self.lang]
        # print(time)
        if self.filetype not in self.base_filetypes:
            time *= 1.2
        if time < min_time:
            time = min_time
        return time

    def calculate_deadline(self, minutes: float) -> datetime:
        dt = datetime.now()
        print('now: ', dt)
        while minutes > 0:
            today_end = datetime(year=dt.year, month=dt.month, day=dt.day, hour=self.end_hours)
            delta = ((today_end - dt).seconds / 60)
            if delta > minutes:
                dt += timedelta(minutes=minutes)
            else:
                dt += timedelta(minutes=delta) + timedelta(hours=24 - self.end_hours + self.start_hours)
                if dt.weekday() == self.end_day + 1:
                    dt += timedelta(days=6 - self.end_day + self.start_day)
            minutes -= delta
            # print(dt)
            # print(minutes)
        return dt


doc = Document('docx', 500, 3)
print('price = ', doc.calculate_price(), ' UAH')
ex_time = doc.calculate_time()
print('Execution time = ', ex_time, ' minutes')
print('deadline = ', doc.calculate_deadline(ex_time))
