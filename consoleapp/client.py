import consoleapp.settings as settings


class HomeAccount:

    def show_menu(self):
        """Показать меню"""
        for idx, item in enumerate(settings.MENU, 1):
            print(idx, item["name"])


if __name__ == "__main__":
    ha = HomeAccount()
    ha.show_menu()
    while True:
        user_select = input("# ")
        if user_select.isdigit():
            select = int(user_select[:1]) - 1
            if 0 <= select < len(settings.MENU):
                break

    scenario_name = settings.MENU[select]["scenario"]
    next_step_name = settings.SCENARIOS[scenario_name]["first_step"]
    next_step = settings.SCENARIOS[scenario_name]["steps"][next_step_name]
    print(next_step["text"])
