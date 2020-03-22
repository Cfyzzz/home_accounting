from datetime import datetime

import consoleapp.settings as settings
import re

from models import CashItem, ManagerCashItems, NamesCashItem


PREF = "# "
PATTERN_DATE = r'(0?[1-9]|1[0-2]).\d{4}'
DATE_FORMAT = f'^{PATTERN_DATE}$'
PERIOD_FORMAT = f'^{PATTERN_DATE} {PATTERN_DATE}$'


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

            print("\tВыберете статью:")
            cashitem_names = NamesCashItem.select()
            for idx, item in enumerate(cashitem_names, 1):
                print('\t', idx, item.name)

            select = self._get_user_select(cashitem_names, extend=['[Выход]'])
            if select == len(cashitem_names):
                step["next_step"] = None
                return

            self.current_cashitem_name = cashitem_names[select]

        if step["function_name"] == "set summa":
            print("\tУкажите общую сумму на заданный период по статье")
            user_summa = ""
            while not user_summa.isdigit():
                user_summa = input(PREF)

            summa = int(user_summa)
            manager.planning(self.current_cashitem_name, summa)

    def _get_user_select(self, items, extend=[]):
        for idx, ext in enumerate(extend, len(items) + 1):
            print("\t", idx, ext)

        while True:
            user_select = input(PREF)
            max_value = len(items) + len(extend)
            if user_select.isdigit():
                select = int(user_select[:1]) - 1
                if 0 <= select < max_value:
                    return select

    def new_cashitem(self):
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

