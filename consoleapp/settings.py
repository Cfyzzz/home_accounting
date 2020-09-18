import logging


MENU = [
    {
        "name": "Планирование",
        "scenario": "plan"
    },
    {
        "name": "Списание",
        "scenario": "write-off"
    },
    {
        "name": "Распределить приход",
        "scenario": "distribute income"
    },
    {
        "name": "Просмотр",
        "scenario": "review"
    },
    # {
    #     "name": "Редактирование",
    #     "scenario": "edit"
    # },
    {
        "name": "Перенос остатков между статьями",
        "scenario": "carryover of residues",
    },
    {
        "name": "Настройка статей",
        "scenario": "setting"
    },
    # {
    #     "name": "Копирование предыдущего периода",
    #     "scenario": "copy previous period"
    # }
]

SCENARIOS = {
    "plan": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Выбрать период",
                "function_name": "select period",
                "next_step": "step2"
            },
            "step2": {
                "text": "Выбрать статью",
                "function_name": "select cashitem",
                "next_step": "step3"
            },
            "step3": {
                "text": "Указать сумму",
                "function_name": "set summa",
                "next_step": "step2"
            }
        }
    },
    "write-off": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Выбрать месяц",
                "function_name": "select month",
                "next_step": "step2"
            },
            "step2": {
                "text": "Выбрать статью",
                "function_name": "select cashitem",
                "next_step": "step3"
            },
            "step3": {
                "text": "Указать сумму",
                "function_name": "write-off summa",
                "next_step": "step4"
            },
            "step4": {
                "text": "Просмотр",
                "function_name": "view period",
                "next_step": None
            }
        }
    },
    "distribute income": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Выбрать период",
                "function_name": "select period",
                "next_step": "step2"
            },
            "step2": {
                "text": "Укажите сумму распределения",
                "function_name": "distribute money",
                "next_step": None
            }
        }
    },
    "carryover of residues": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Выбрать месяц",
                "function_name": "select month",
                "next_step": "step2"
            },
            "step2": {
                "text": "Просмотр",
                "function_name": "view period",
                "next_step": "step3"
            },
            "step3": {
                "text": "Перенос суммы между статьями",
                "function_name": "carryover of residues",
                "next_step": None
            },
        },
    },
    # "edit": {
    #     "first_step": "step1",
    #     "steps": {
    #         "step1": {
    #             "text": "Выбрать период",
    #             "next_step": "step2"
    #         },
    #         "step2": {
    #             "text": "Выбрать статью",
    #             "next_step": "step3"
    #         },
    #         "step3": {
    #             "text": "Указать сумму",
    #             "next_step": None
    #         }
    #     }
    # },
    "review": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Выбрать период",
                "function_name": "select period",
                "next_step": "step2"
            },
            "step2": {
                "text": "Просмотр",
                "function_name": "view period",
                "next_step": None
            }
        }
    },
    "setting": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Настроить статьи",
                "function_name": "cash items settings",
                "next_step": None
            }
        }
    },
    # "copy previous period": {
    #     "first_step": "step1",
    #     "steps": {
    #         "step1": {
    #             "text": "Выбрать месяц-образец",
    #             "function_name": "select month",
    #             "next_step": "step2"
    #         },
    #         "step2": {
    #             "text": "Выбрать новый месяц",
    #             "function_name": "select new month",
    #             "next_step": "step3"
    #         },
    #         "step3": {
    #             "text": "Копировать статьи",
    #             "function_name": "copy items",
    #             "next_step": None
    #         }
    #     }
    # }
}


logger = logging.getLogger("home_accounting")
log_path = 'home_accounting_console.log'
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

logger.addHandler(file_handler)


def log(message):
    logger.warning(message)
