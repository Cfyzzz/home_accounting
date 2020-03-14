class ControlManager:

    def distribute_money(self, rows, money):
        """Разнести приход по статьям

        :param rows: записи, среди которых нужно распределить деньги
        :param money: сумма распределения
        """

    def flow(self, row_source, row_dest, summa, check_summa=True):
        """Проводка движения денег между статьями

        :param row_source: запись-источник
        :param row_dest: запись-приёмник
        :param summa: сумма проводки
        :param check_summa: проверять проводку
        """
        is_valid = True
        if check_summa and (row_source.value + row_source.virtual_value - row_source.min_value) < summa:
            is_valid = False

        if is_valid:
            row_source.value -= summa
            row_source.save()

            row_dest.value += summa
            row_dest.save()

        return is_valid
