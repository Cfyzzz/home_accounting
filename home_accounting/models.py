from django.db import models


class CashItem(models.Model):
    name = models.CharField(default="", unique=True, verbose_name=u"Название статьи")
    min_value = models.IntegerField(verbose_name=u"Минимальный порог")
    value = models.IntegerField(verbose_name=u"Значение")
    plan_value = models.IntegerField(verbose_name=u"Плановое значение")
    date = models.DateField(verbose_name=u"Период")
    virtual_value = models.IntegerField(verbose_name=u"Плановый приход")

    def __unicode__(self):
        return self.name

    class Mets:
        verbose_name = u"статья"
        verbose_name_plural = u"статьи"


class ManagerCashItems(models.Model):
    date_begin = models.DateField(verbose_name=u"Начало периода")
    date_end = models.DateField(verbose_name=u"Конец периода")
    cash_items = models.ForeignKey(CashItem, on_delete=models.CASCADE)

    def __unicode__(self):
        return f"{self.date_begin} - {self.date_end}"

    def set_period_manager(self, begin, end):
        """Установить период текущего менеджера

        :param begin: начало периода
        :param end: конец периода
        """

    def append(self, row):
        """Добавить запись в менеджер

        :param row: добавляемая статья
        """

    def remove(self, row):
        """Удалить запись из менеджера

        :param row: удаляемая запись
        """

    def replace(self, old_row, new_row):
        """Переписать запись

        :param old_row: старая запись
        :param new_row: новая запись
        """

    def copy(self, row):
        """Скопировать запись таблицы менеджера

        :param row: копируемая запись
        :return CashItem: новая запись
        """

    class Mets:
        verbose_name = u"менеджер планирования"
        verbose_name_plural = u"менеджеры планирования"


class ControlManager(models.Model):
    user = models.CharField()
    managers = models.ForeignKey(CashItem, on_delete=models.CASCADE)

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
