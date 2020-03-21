import math
from datetime import datetime

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


class CashItem(BaseTable):
    name = peewee.ForeignKeyField(NamesCashItem)
    min_value = peewee.IntegerField(default=0, verbose_name="Минимальный порог")
    value = peewee.IntegerField(default=0, verbose_name=u"Значение")
    plan_value = peewee.IntegerField(default=0, verbose_name=u"Плановое значение")
    date = peewee.DateField(default=datetime.today(), verbose_name="Период")
    virtual_value = peewee.IntegerField(default=0, verbose_name=u"Плановый приход")

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
        number_months = 12*(self.date_end.year-self.date_begin.year)+(self.date_end.month-self.date_begin.month)+1
        plan_item = math.ceil(plan / number_months)
        for _ in range(number_months):
            pass
            # TODO - Проверить, что есть такая статья и переопределить сумму
            #  или созадть статью с суммой

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

        :return value, plan_value, virtual_value
        """
        self.update()
        total_info = ((ci.value, ci.plan_value, ci.virtual_value) for ci in self.cash_items)
        value, plan_value, virtual_value = map(sum, zip(*total_info))
        return value, plan_value, virtual_value

    def update(self):
        """Обновить состав статей"""
        self.cash_items = list(CashItem.select().where(self.date_begin < CashItem.date < self.date_end))

    class Mets:
        verbose_name = u"менеджер планирования"
        verbose_name_plural = u"менеджеры планирования"
