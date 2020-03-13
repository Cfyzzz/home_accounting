from django.db import models

from cashitem.models import CashItem


class ManagerCashItems(models.Model):
    date_begin = models.DateField(verbose_name=u"Начало периода")
    date_end = models.DateField(verbose_name=u"Конец периода")
    cash_item = models.ForeignKey(CashItem, on_delete=models.CASCADE)

    def __unicode__(self):
        return f"{self.date_begin} - {self.date_end}"

    def set_period_manager(self, begin, end):
        """Установить период текущего менеджера

        :param begin: начало периода
        :param end: конец периода
        """
        self.date_begin = begin
        self.date_end = end
        self.save()

    def replace(self, dest_cash_item, source_cash_item):
        """Переписать запись таблицы менеджера

        :param dest_cash_item: запись-приёмник
        :param source_cash_item: запись-источник
        """
        dest_cash_item.min_value = source_cash_item.min_value
        dest_cash_item.value = source_cash_item.value
        dest_cash_item.plan_value = source_cash_item.plan_value
        dest_cash_item.date = source_cash_item.date
        dest_cash_item.virtual_value = source_cash_item.virtual_value
        dest_cash_item.save()

    def copy(self, row):
        """Скопировать запись таблицы менеджера

        :param row: копируемая запись
        :return CashItem: новая запись
        """

    class Mets:
        verbose_name = u"менеджер планирования"
        verbose_name_plural = u"менеджеры планирования"


class ControlManager(models.Model):
    user = models.CharField(max_length=40)
    manager = models.ForeignKey(CashItem, on_delete=models.CASCADE)

    def create_manager(self):
        """Создать менеджера"""

    def get_managers(self):
        """Получить список менеджеров"""

    def delete_manager(self, manager):
        """Удалить менеджера

        :param manager: удаляемый менеджер
        """

    def copy_manager(self, manager):
        """Копирование менеджера

        :param manager: копируемый менеджер
        :return ManagerCashItems: новый менеджер
        """

    def get_managers_by_date(self, date):
        """Получить всех менеджеров по дате

        :param date: дата, на которую получаем менеджеров
        :return list of ManagerCashItems
        """

    def get_total_manager_by_date(self, date):
        """Получить сводную информацию по всем менеджерам на дату

        :param date: дата, на которую получаем менеджеров
        :return list of CashItem
        """

    def distribute_money(self, rows, money):
        """Разнести приход по статьям

        :param rows: записи, среди которых нужно распределить деньги
        :param money: сумма распределения
        """

    def flow(self, row_source, row_dest):
        """Проводка движения денег между статьями

        :param row_source: запись-источник
        :param row_dest: запись-приёмник
        """

    def append(self, cash_item):
        """Добавить запись в менеджер

        :param cash_item: добавляемая статья
        """
        row = ManagerCashItems(date_begin=self.manager.date_begin, date_end=self.manager.date_end, cash_item=cash_item)
        row.save()

    def remove(self, cash_item):
        """Удалить запись из менеджера

        :param cash_item: удаляемая запись
        """
        row = ManagerCashItems.objects.filter(cash_item=cash_item)
        row.delete()
