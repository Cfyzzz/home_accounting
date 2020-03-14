from cashitem.models import CashItem, NamesCashItem


class ManagerCashItems:

    def __init__(self, date_begin, date_end):
        self.date_begin = date_begin
        self.date_end = date_end
        self.cash_items = []
        self.update()

    def __unicode__(self):
        return f"{self.date_begin} - {self.date_end}"

    def set_period_manager(self, begin, end):
        """Установить период текущего менеджера

        :param begin: начало периода
        :param end: конец периода
        """
        self.date_begin = begin
        self.date_end = end
        self.update()

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
        self.cash_items = list(CashItem.objects.filter(date__range=(self.date_begin, self.date_end)))

    class Mets:
        verbose_name = u"менеджер планирования"
        verbose_name_plural = u"менеджеры планирования"
