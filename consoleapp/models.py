import math
from datetime import datetime, timedelta

import peewee

database = peewee.SqliteDatabase("test.sqlite3")


class BaseTable(peewee.Model):
    # В подклассе Meta указываем подключение к той или иной базе данных
    class Meta:
        database = database


class NamesCashItem(BaseTable):
    name = peewee.CharField()

    class Meta:
        verbose_name = u"Название статьи"
        verbose_name_plural = u"Названия статей статей"
        database = database

    def __str__(self):
        return self.name


class CashItem(BaseTable):
    name = peewee.ForeignKeyField(NamesCashItem)
    min_value = peewee.IntegerField(default=0, verbose_name="Минимальный порог")
    value = peewee.IntegerField(default=0, verbose_name=u"Значение")
    plan_value = peewee.IntegerField(default=0, verbose_name=u"Плановое значение")
    date = peewee.DateField(default=datetime.today(), verbose_name="Период")
    virtual_value = peewee.IntegerField(default=0, verbose_name=u"Плановый приход")
    active = peewee.BooleanField(default=True)

    class Meta:
        verbose_name = u"статья"
        verbose_name_plural = u"статьи"
        database = database


database.connect()
database.create_tables([NamesCashItem, CashItem])


#
# class NamesCashItem:
#
#     def __init__(self, name):
#         self.name = name
#
#     def __unicode__(self):
#         return self.name
#
#
# class CashItem:
#
#     def __init__(self,
#                  name=None,
#                  min_value=0,
#                  value=0,
#                  plan_value=0,
#                  date=datetime.today(),
#                  virtual_value=0):
#         self.name = name
#         self.min_value = min_value
#         self.value = value
#         self.plan_value = plan_value
#         self.date = date
#         self.virtual_value = virtual_value
#
#     def __str__(self):
#         return self.name


class ManagerCashItems:

    def __init__(self):
        self.date_begin = None
        self.date_end = None
        self.cash_items = []

    def __str__(self):
        return f"{self.date_begin} - {self.date_end}"

    def set_period_manager(self, begin, end):
        """Установить период текущего менеджера

        :param begin: начало периода
        :param end: конец периода
        """
        self.date_begin = begin
        self.date_end = end
        self.update()

    def planning(self, name_item, plan):
        """Планирование суммы по статье на установленный период

        :param name_item: название статьи (строка)
        :param plan: планируемая сумма на период
        """
        number_months = 12 * (self.date_end.year - self.date_begin.year) + (
                    self.date_end.month - self.date_begin.month) + 1
        plan_item = math.ceil(plan / number_months)
        for delta in range(number_months):
            month = self.date_begin.month + delta
            year = self.date_begin.year
            if month > 12:
                month = month % 12
                year += month // 12

            date_item = datetime(year, month, 1).date()
            data = {'date': date_item, 'plan_value': plan_item, 'name': name_item}
            CashItem.insert(data).execute()

    def append(self, name_item, date_item):
        """Добавить запись в менеджер

        :param date_item: дата записи
        :param name_item: название статьи (строка)
        """
        name_cashitem = NamesCashItem.objects.filter(name=name_item)
        if name_cashitem.exists():
            name_cashitem = name_cashitem[0]
        else:
            name_cashitem = NamesCashItem(name=name_item)
            name_cashitem.save()

        row = CashItem(name=name_cashitem, date=date_item)
        row.save()
        self.update()
        return row

    def remove(self, cash_item):
        """Удалить запись из менеджера

        :param cash_item: удаляемая запись
        """
        cash_item.delete()
        self.update()

    def replace(self, dest_cash_item, source_cash_item):
        """Переписать запись таблицы менеджера. Статья не меняется!

        :param dest_cash_item: запись-приёмник
        :param source_cash_item: запись-источник
        """
        dest_cash_item.min_value = source_cash_item.min_value
        dest_cash_item.value = source_cash_item.value
        dest_cash_item.plan_value = source_cash_item.plan_value
        dest_cash_item.date = source_cash_item.date
        dest_cash_item.virtual_value = source_cash_item.virtual_value
        dest_cash_item.save()

    def copy(self, source_cash_item):
        """Скопировать запись таблицы менеджера. Запись сама не сохранеяяется!

        :param source_cash_item: копируемая запись
        :return CashItem: новая запись
        """
        dest_cash_item = CashItem(name=source_cash_item.name,
                                  date=source_cash_item.date,
                                  min_value=source_cash_item.min_value,
                                  value=source_cash_item.value,
                                  plan_value=source_cash_item.plan_value,
                                  virtual_value=source_cash_item.virtual_value)
        return dest_cash_item

    def get_total(self):
        """Получить сводную информацию по периоду

        :return value, plan_value, virtual_value, min_value
        """
        self.update()
        total_info = ((ci.value, ci.plan_value, ci.virtual_value, ci.min_value) for ci in self.cash_items)
        value, plan_value, virtual_value, min_value = map(sum, zip(*total_info))
        return value, plan_value, virtual_value, min_value

    def get_sorting_rows(self):
        """Возвращает отсортированную таблицу
        [Номер строки, Статья, Дата, План, Текущее значение]
        """
        self.update()
        col_dates, rows = self._get_rows_from_current_cashitems()
        table = self._get_table_by_format_from_dates_and_rows(col_dates, rows)
        return table

    @staticmethod
    def _get_table_by_format_from_dates_and_rows(col_dates, rows):
        table = [["№", u"Статья"]]
        table[0].extend(col_dates)
        current_number = 0
        total_row = [[0, 0, 0] for _ in range(len(col_dates) + 1)]
        table[0].append(u"Всего")
        for row in rows:
            new_row = [row['number'], row['name']]
            sum_row = [0, 0, 0]
            for date in col_dates:
                sub_row = [0, 0, 0]
                if row['date'] == date:
                    sub_row = [row['plan'], row['value'], row['min_value']]
                new_row.append(sub_row)
                sum_row = list(map(sum, zip(sub_row, sum_row)))

            new_row.append(sum_row)
            if row['number'] == current_number:
                recent_row = table[-1]
                result_row = list(
                    map(lambda a: [a[0][0] + a[1][0], a[0][1] + a[1][1], a[0][2] + a[1][2]],
                        zip(recent_row[2:], new_row[2:])))
                table[-1][2:] = result_row
            else:
                current_number = row['number']
                table.append(new_row)

            total_row = list(map(lambda a: [a[0][0] + a[1][0], a[0][1] + a[1][1], a[0][2] + a[1][2]],
                                 zip(new_row[2:], total_row)))

        split_line = ["---"] * (len(col_dates) + 3)
        table.append(split_line)
        total = ["", "ИТОГО"]
        total.extend(total_row)
        table.append(total)
        return table

    def _get_rows_from_current_cashitems(self):
        rows = []
        row_numbers = {}
        current_number = 0
        col_dates = []
        for cashitem in self.cash_items:
            name = cashitem.name.name
            if not name in row_numbers:
                current_number += 1
                row_numbers[name] = current_number

            date = cashitem.date
            if not date in col_dates:
                col_dates.append(date)

            number = row_numbers[name]
            row = dict(
                number=number,
                name=cashitem.name.name,
                date=cashitem.date,
                plan=cashitem.plan_value,
                value=cashitem.value + cashitem.virtual_value,
                min_value=cashitem.min_value
            )
            rows.append(row)
        col_dates.sort()
        rows.sort(key=lambda x: x['number'])
        return col_dates, rows

    def writeoff(self, summa, cashitem_name):
        """Списание средств по статье

        :param summa: сумма списания
        :param cashitem_name: статья списания
        """
        cashitem = CashItem.get(name=cashitem_name, date=self.date_begin)
        cashitem.min_value += summa
        cashitem.value -= summa
        cashitem.save()

    def move(self, source_cashitem_name, dest_cashitem_name, summa):
        source_cashitem = CashItem.get(name=source_cashitem_name, date=self.date_begin)
        source_cashitem.value -= summa
        source_cashitem.save()
        dest_cashitem = CashItem.get(name=dest_cashitem_name, date=self.date_begin)
        dest_cashitem.value = summa
        dest_cashitem.save()

    def offer_to_distribute_money(self, summa):
        """Предлагает распеределение суммы между статьями

        :param summa: сумма к распределению
        :return {cashitem_name: {plan, balance_plan, share}, ...}
        """
        self.update()
        value, plan_value, virtual_value, min_value = self.get_total()
        balance_plan = plan_value - (value + min_value)
        summa = min(summa, balance_plan)
        accum = 0
        values = {}
        for cashitem in self.cash_items:
            _koeff = (cashitem.plan_value - (cashitem.value + cashitem.min_value)) / balance_plan
            _share = round(summa * _koeff)
            if cashitem.name not in values:
                values[cashitem.name] = dict(
                    plan=cashitem.plan_value,
                    balance_plan=cashitem.plan_value - (cashitem.value + cashitem.min_value),
                    share=_share
                )
            else:
                values[cashitem.name]['plan'] += cashitem.plan_value
                values[cashitem.name]['balance_plan'] += cashitem.plan_value - (cashitem.value + cashitem.min_value)
                values[cashitem.name]['share'] += _share
            accum += _share
        else:
            if len(self.cash_items):
                values[self.cash_items[-1].name]['share'] += summa - accum

        return values

    def distribute_money(self, cashitem_name, summa):
        """Распределяет сумму по статьям с указанным именем за период

        :param cashitem_name: имя статьи
        :param summa: сумма распределения
        """

        cashitems = list(CashItem.select().where(
            CashItem.date.between(self.date_begin, self.date_end) & (CashItem.name == cashitem_name)))
        if len(cashitems) == 0:
            print(f"!!! Распределить по статье {cashitem_name} не удалось")
            return

        share = summa // len(cashitems)
        accum = 0
        delta = 0
        for cashitem in cashitems:
            _share = share + delta
            clac_share = max(0, min(_share, cashitem.plan_value - cashitem.value))
            delta = _share - clac_share
            cashitem.value += clac_share
            accum += clac_share
            cashitem.save()

        if accum < summa:
            share = accum
            for cashitem in cashitems:
                if cashitem.plan_value <= cashitem.value:
                    continue
                clac_share = max(0, min(share, cashitem.plan_value - cashitem.value))
                share -= clac_share
                cashitem.value += clac_share
                accum += clac_share
                cashitem.save()

            cashitems[0].value += summa - accum
            cashitems[0].save()

    def update(self):
        """Обновить состав статей"""
        self.cash_items = list(CashItem.select().where(CashItem.date.between(self.date_begin, self.date_end)))

    def get_all_cashitems(self):
        return list(NamesCashItem.select())

    class Mets:
        verbose_name = u"менеджер планирования"
        verbose_name_plural = u"менеджеры планирования"
