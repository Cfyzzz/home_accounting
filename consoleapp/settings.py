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
        "name": "Просмотр",
        "scenario": "review"
    },
    {
        "name": "Редактирование",
        "scenario": "edit"
    },
    {
        "name": "Настройка статей",
        "scenario": "setting"
    }
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
                "next_step": "ste2"
            },
            "step2": {
                "text": "Выбрать статью",
                "next_step": "step3"
            },
            "step3": {
                "text": "Указать сумму",
                "next_step": None
            }
        }
    },
    "edit": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Выбрать период",
                "next_step": "ste2"
            },
            "step2": {
                "text": "Выбрать статью",
                "next_step": "step3"
            },
            "step3": {
                "text": "Указать сумму",
                "next_step": None
            }
        }
    },
    "review": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Выбрать период",
                "next_step": None
            }
        }
    },
    "setting": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Настроить статьи",
                "next_step": None
            }
        }
    }
}
