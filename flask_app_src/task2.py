# 1 - rus, 2 - ukr, 3 -eng
from datetime import datetime, timedelta


class Document(object):

    base_filetypes = ['doc', 'docx', 'rtf']

    # lang = {
    #    'Rus': 1,
    #    'Ukr': 2,
    #    'Eng': 3,
    #  }

    lang = [1, 2, 3]

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
        if num_sym <= 0:
            raise Exception('The number of symbols must be more than 0!')
        else:
            self.num_sym = num_sym
        if lang not in self.lang:
            raise Exception('Unknown language')
        else:
            self.lang = lang

    def calculate_price(self) -> float:
        price = self.num_sym * self.price_sym[self.lang]
        # print(price)
        if self.filetype not in self.base_filetypes:
            price *= 1.2
        return round(max(price, self.min_prices[self.lang]), 2)

    def calculate_time(self) -> float:
        min_time = 60
        time = 30 + self.num_sym/self.speed[self.lang]
        # print(time)
        if self.filetype not in self.base_filetypes:
            time *= 1.2
        return round(max(time, min_time),2)

    def calculate_deadline(self, dt: datetime, minutes: float) -> datetime:
        print('Order get at: ', dt)

        if dt.hour < self.start_hours:
            dt = datetime(year=dt.year, month=dt.month, day=dt.day, hour=self.start_hours)
        if dt.hour >= self.end_hours:
            dt += timedelta(days=1)
            dt = datetime(year=dt.year, month=dt.month, day=dt.day, hour=self.start_hours)
        if dt.weekday() not in range(self.start_day, self.end_day+1):
            dt += timedelta(days=7 - dt.weekday() + self.start_day)
            dt = datetime(year=dt.year, month=dt.month, day=dt.day, hour=self.start_hours)
        print('Work starts at: ', dt)

        while minutes > 0:
            today_end = datetime(year=dt.year, month=dt.month, day=dt.day, hour=self.end_hours)
            delta = ((today_end - dt).seconds / 60)
            if delta >= minutes:
                dt += timedelta(minutes=minutes)
            else:
                dt += timedelta(minutes=delta) + timedelta(hours=24 - self.end_hours + self.start_hours)
                if dt.weekday() == self.end_day + 1:
                    dt += timedelta(days=6 - self.end_day + self.start_day)
            minutes -= delta
            # print(dt)
            # print(minutes)
        return dt


# doc = Document('docx', 4000, 3)
# print('price = ', doc.calculate_price(), ' UAH')
# ex_time = doc.calculate_time()
# print('Execution time = ', ex_time, ' minutes')
# print('deadline = ', doc.calculate_deadline(datetime(2020, 9, 7, 13, 12), ex_time))


def test_1():
    doc = Document('docx', 100, 1)
    assert doc.calculate_price() == 50
    assert doc.calculate_time() == 60


def test_2():
    doc = Document('docx', 100, 3)
    assert doc.calculate_price() == 120
    assert doc.calculate_time() == 60


def test_3():
    doc = Document('docx', 1500, 1)
    assert doc.calculate_price() == 75
    assert doc.calculate_time() == 97.52


def test_4():
    doc = Document('xlsx', 1500, 1)
    assert doc.calculate_price() == 75 * 1.2
    assert doc.calculate_time() == 117.02


def test_5():
    doc = Document('xlsx', 1500, 3)
    assert doc.calculate_price() == 216
    assert doc.calculate_time() == 360.32


def test_6():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 7, 17, 40)  # Mon, 7th of September, 2020, 17-40
    ex_time = 200
    expected_date = datetime(2020, 9, 8, 12, 0)  # Tue, 8th of September, 2020, 12-00
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


def test_7():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 4, 17, 40)  # Fri, 4th of September, 2020, 17-40
    ex_time = 200
    expected_date = datetime(2020, 9, 7, 12, 0)  # Mon, 7th of September, 2020, 12-00
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


def test_8():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 4, 9, 40)  # Fri, 4th of September, 2020, 9-40
    ex_time = 120
    expected_date = datetime(2020, 9, 4, 12, 0)  # Fri, 4th of September, 2020, 12-00
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


def test_9():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 5, 16, 30)  # Sat, 5th of September, 2020, 16-30
    ex_time = 12*60
    expected_date = datetime(2020, 9, 8, 13, 0)  # Tue, 8th of September, 2020, 13-00
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


def test_10():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 4, 9, 40)  # Fri, 4th of September, 2020, 9-40
    ex_time = 20*60
    expected_date = datetime(2020, 9, 8, 12, 0)  # Tue, 8th of September, 2020, 12-00
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


def test_11():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 4, 18, 59)  # Fri, 4th of September, 2020, 9-40
    ex_time = 2
    expected_date = datetime(2020, 9, 7, 10, 1)  # Mon, 7th of September, 2020, 10-01
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


def test_12():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 2, 19, 32)  # Wed
    ex_time = 157
    expected_date = datetime(2020, 9, 3, 12, 37)  # Thu
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


def test_13():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 2, 0, 41)  # Wed
    ex_time = 157
    expected_date = datetime(2020, 9, 2, 12, 37)  # Wed
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


def test_14():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 6, 0, 41)  # Sun
    ex_time = 322
    expected_date = datetime(2020, 9, 7, 15, 22)  # Mon
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


def test_15():
    doc = Document('docx', 100, 1)
    start_date = datetime(2020, 9, 2, 22, 51)  # Wed
    ex_time = 157
    expected_date = datetime(2020, 9, 3, 12, 37)  # Thu
    assert doc.calculate_deadline(start_date, ex_time) == expected_date


