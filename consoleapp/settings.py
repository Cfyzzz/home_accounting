MENU = [
    {
        "name": "Планирование",
        "scenario": "plan"
    },
    {
        "name": "Списание",
        "scenario": None
    },
    {
        "name": "Просмотр",
        "scenario": None
    },
    {
        "name": "Редактирование",
        "scenario": None
    },
    {
        "name": "Настройка статей",
        "scenario": None
    }
]

SCENARIOS = {
    "plan": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "",
                "next_step": "step2"
            },
            "step2": {
                "text": "",
                "next_step": "step3"
            }
        }
    }
}
