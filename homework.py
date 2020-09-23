import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum (
            record.amount for record in self.records
            if record.date == today
            )

    def get_week_stats(self):
        today = dt.date.today()
        one_week_ago = today - dt.timedelta(days=7)
        return sum (
            record.amount for record in self.records
            if one_week_ago <= record.date <= today
            )

    def _today_remained(self):
       return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 70.00
    EURO_RATE = 89.00
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        cash_remained = self._today_remained()
        
        CURRENCIES = {
            'usd': ['USD', self.USD_RATE],
            'rub': ['руб', self.RUB_RATE],
            'eur': ['Euro', self.EURO_RATE]
            }

        if currency not in CURRENCIES:
            raise ValueError

        currency_name, rate = CURRENCIES[currency]

        if cash_remained == 0:
            return 'Денег нет, держись'

        remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            return f'На сегодня осталось {remained} {currency_name}'
        elif cash_remained < 0:
            cash = abs(remained)
            return f'Денег нет, держись: твой долг - {cash} {currency_name}'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_remained = self._today_remained()

        if calories_remained > 0:
            return (
                f'Сегодня можно съесть что-нибудь ещё, ' 
                f'но с общей калорийностью не более {calories_remained} кКал'
                )
        return 'Хватит есть!'


class Record:
    
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = self.set_dt(date)
        
    def set_dt(self, date):
        if date is None:
            return dt.date.today()
        return dt.datetime.strptime (date, '%d.%m.%Y').date()
