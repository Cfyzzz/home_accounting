from datetime import datetime

import consoleapp.settings as settings
import re

from models import CashItem, ManagerCashItems, NamesCashItem
from prettytable import PrettyTable


PREF = "# "
PATTERN_DATE = r'(0?[1-9]|1[0-2]).\d{4}'
DATE_FORMAT = f'^{PATTERN_DATE}$'
PERIOD_FORMAT = f'^{PATTERN_DATE} {PATTERN_DATE}$'

LITER_AUTO = 'A'

COMMENT_UNDER_TABLE_FOLOW = ("[y(д) - commit], [n(н) - cancel], [cashitem summa [other_cashitem(s)]]\n"
            + "1 1000 - оставить на статье №1 сумму 1000 из поступления, остальное распределить по статьям А\n"
            + "1 2000 3 - оставить на статье №1 сумму 2000, остальное распределить на статью №3\n"
            + "1 3000 2 4 - оставить на статье №1 сумму 3000, остальное распределить на статьи №2 и №4")

manager = ManagerCashItems()


class HomeAccountConsole:

    def __init__(self):
        self.period = []
        self.current_cashitem_name = None

    def show_menu(self):
        """Показать меню"""
        for idx, item in enumerate(settings.MENU, 1):
            print('\t', idx, item["name"])

        return self._get_user_select(settings.MENU)

    def execute_step(self, step):
        print(step["text"])
        print('-' * len(step["text"]))
        if step["function_name"] == "select period":
            print("\tУкажите период в формате:\n\tmm.yyyy mm.yyyy (на один месяц нужно указать только одну дату)")
            user_line = ""
            while not (re.fullmatch(PERIOD_FORMAT, user_line)
                       or re.fullmatch(DATE_FORMAT, user_line)):
                user_line = input(PREF)

            dates = [datetime.strptime(m.group(), '%m.%Y').date() for m in re.finditer(PATTERN_DATE, user_line)]
            if len(dates) == 1:
                dates = dates*2

            if dates[0] > dates[1]:
                dates.reverse()

            self.period = dates
            manager.set_period_manager(*self.period)
            return

        if step["function_name"] == "select cashitem":
            if NamesCashItem.select().count() == 0:
                self.new_cashitem()

            print("\tВыберите статью:")
            cashitem_names = list(NamesCashItem.select())
            for idx, item in enumerate(cashitem_names, 1):
                print('\t', idx, item.name)

            select = self._get_user_select(cashitem_names, extend=['[Выход]'])
            if select == len(cashitem_names):
                step["next_step"] = None
                return

            self.current_cashitem_name = cashitem_names[select]

        if step["function_name"] == "view period":
            table = manager.get_sorting_rows()
            table_show = PrettyTable()
            table_show.field_names = table[0]
            for row in table[1:]:
                _row = row[:2]
                for r in row[2:]:
                    _row.append(f"{r[0]}/{r[1]} {r[2]}")
                table_show.add_row(_row)
            print(table_show)
            print("* Расшифровка: [план/накоплено списано]")

        if step["function_name"] == "set summa":
            print("\tУкажите общую сумму на заданный период по статье")
            user_summa = ""
            while not user_summa.isdigit():
                user_summa = input(PREF)

            summa = int(user_summa)
            manager.planning(self.current_cashitem_name, summa)

        if step["function_name"] == "select month":
            print("\tУкажите месяц в формате mm.yyyy")
            user_line = ""
            while not re.fullmatch(DATE_FORMAT, user_line):
                user_line = input(PREF)

            dates = [datetime.strptime(m.group(), '%m.%Y').date() for m in re.finditer(PATTERN_DATE, user_line)]
            dates = dates * 2
            self.period = dates
            manager.set_period_manager(*self.period)
            return

        if step["function_name"] == "write-off summa":
            print("\tУкажите сумму списания")
            user_summa = ""
            while not user_summa.isdigit():
                user_summa = input(PREF)

            summa = int(user_summa)
            manager.writeoff(summa=summa, cashitem_name=self.current_cashitem_name)

        if step["function_name"] == "distribute money":
            # print("\tУкажите сумму распределения")
            user_summa = ""
            while not user_summa.isdigit():
                user_summa = input(PREF)

            summa = int(user_summa)
            balance = manager.offer_to_distribute_money(summa)
            table = self._make_table(balance)
            print(table)
            print(COMMENT_UNDER_TABLE_FOLOW)
            commit = self._user_input_distribute_money(table)
            if commit:
                self._commit(table)

        if step["function_name"] == "cash items settings":
            submenu = ["Новая статья"]
            # TODO - Добавить изменить активность статьи
            # TODO - Добавить Переименовать статью
            # TODO - Скопировать статьи на следующий период (копируется план и указанные статьи)
            # TODO - Выбрать статью и указать что будем корректировать: план или текущее значение
            while True:
                print("\tДействующие статьи:")
                cashitems_names = manager.get_all_cashitems()
                if len(cashitems_names) == 0:
                    print("\t-- Нет статей --")
                else:
                    for name in cashitems_names:
                        print(f"\t   {name}")
                print()
                print("\tВыберите действие:")
                for idx, item in enumerate(submenu, 1):
                    print('\t', idx, item)

                select = self._get_user_select(submenu, extend=['[Выход]'])
                if select == len(submenu):
                    step["next_step"] = None
                    return

                if select == 0:
                    self.new_cashitem()

    def _user_input_distribute_money(self, table):
        """Работа пользователя с таблицей распределения"""

        is_valid = False
        commit = False
        while not is_valid:
            user_line = input(PREF)
            if user_line in 'yYдД':
                commit = True
                is_valid = True
            elif user_line in 'nNнН':
                is_valid = True

            parse_line = re.finditer(r"\d*", user_line)
            input_values = [int(r.group()) for r in parse_line if r.group() and r.group().isdigit()]
            if len(input_values) == 2:
                self._flow_to_other(table, input_values)
            elif len(input_values) > 2:
                self._flow_set(table, input_values)
            else:
                continue

            print(table)
            print(COMMENT_UNDER_TABLE_FOLOW)
        return commit

    def _flow_to_other(self, table: PrettyTable, values):
        """Перекидывает деньги со строки values[0] суммой values[1] на статьи, отмеченные А

        :param table: таблица распределения
        :param values: [номер_строки, сумма]
        """

        rows2 = []
        total_balance_plan = 0
        for row2 in table._rows:
            if not str(row2[0]).isdigit() or row2[0] == values[0]:
                continue

            if row2[5] == LITER_AUTO and row2[3] > 0:
                rows2.append(row2)
                total_balance_plan += row2[3]
        self._folow_pattern(table=table, values=values, rows2=rows2, total_balance_plan=total_balance_plan)

    def _flow_set(self, table, values):
        """Перекидывает деньги со строки values[0] суммой values[1] на указанные статьи

        :param table: таблица распределения
        :param values: [номер_строки, сумма, ...]
        """

        rows2 = []
        total_balance_plan = 0
        for idx in values[2:]:
            if len(table._rows) < idx:
                print("! Неправильно указана целевая статья")
                return

            row2 = table._rows[idx - 1]
            row2[5] = ""
            rows2.append(row2)
            total_balance_plan += row2[3]
        self._folow_pattern(table=table, values=values, rows2=rows2, total_balance_plan=total_balance_plan)

    def _folow_pattern(self, table, values, rows2, total_balance_plan):
        if len(table._rows) < values[0]:
            print("! Неправильно указана статья")
            return
        row = table._rows[values[0] - 1]
        summa = values[1]
        rest_summa = row[4] - summa
        # print(row)  # [0, <NamesCashItem: 1>, 3000, 3000, 1000, 'A']
        row[5] = ""
        row[4] = summa

        if total_balance_plan == 0:
            print("Сумма распределния нулевая")
        else:
            accum = 0
            for row2 in rows2:
                share = round(row2[3] / total_balance_plan * rest_summa)
                accum += share
                row2[4] += share
            else:
                if len(rows2):
                    rows2[-1][4] += rest_summa - accum

        total_share = 0
        for row in table._rows[:-2]:
            total_share += row[4]
        table._rows[-1][4] = total_share
        return

    def _commit(self, table: PrettyTable):
        """Принимает распределение к статьям

        :param table: таблица распределения
        """

        for row in table._rows:
            if not str(row[0]).isdigit():
                continue
            manager.distribute_money(cashitem_name=row[1], summa=row[4])

    @staticmethod
    def _make_table(balance):
        """Выводит таблицу распределения"""

        table_show = PrettyTable()
        table_show.field_names = ["№", "Статья", "План", "Требуется", "Сумма распр.", "Автораспр."]
        total_plan, total_balance_plan, total_share = 0, 0, 0
        idx = 0
        for cashitem, values in balance.items():
            idx += 1
            row = [idx, cashitem, values['plan'], values['balance_plan'], values['share'], LITER_AUTO]
            table_show.add_row(row)

            total_plan += values['plan']
            total_balance_plan += values['balance_plan']
            total_share += values['share']
        row = ["---"] * 6
        table_show.add_row(row)
        row = ["", "ИТОГО", total_plan, total_balance_plan, total_share, ""]
        table_show.add_row(row)
        table_show.align[table_show.field_names[1]] = "l"
        return table_show

    @staticmethod
    def _get_user_select(items, extend=None):
        if not extend:
            extend = []

        for idx, ext in enumerate(extend, len(items) + 1):
            print("\t", idx, ext)

        while True:
            user_select = input(PREF)
            max_value = len(items) + len(extend)
            if user_select.isdigit():
                select = int(user_select[:1]) - 1
                if 0 <= select < max_value:
                    return select

    @staticmethod
    def new_cashitem():
        caption = "Создание новой статьи"
        print(caption)
        print('-' * len(caption))
        print("\tУкажите название статьи:")
        user_item_name = ""
        while user_item_name == "":
            user_item_name = input(PREF)

        row = NamesCashItem(name=user_item_name)
        row.save()


class UserState:
    def __init__(self):
        self.scenario = None
        self.step = None


if __name__ == "__main__":
    while True:
        # TODO - В главном меню добавить Выход
        # TODO - В главное меню добавить Копировать - копирование статей с одного месяца в другой
        # TODO - Куда списывать излишки суммы распределения
        state = UserState()
        ha = HomeAccountConsole()
        select = ha.show_menu()
        scenario_name = settings.MENU[select]["scenario"]
        state.scenario = settings.SCENARIOS[scenario_name]
        next_step_name = state.scenario["first_step"]
        while next_step_name:
            state.step = state.scenario["steps"][next_step_name]
            ha.execute_step(state.step)
            next_step_name = state.step['next_step']
        print()
