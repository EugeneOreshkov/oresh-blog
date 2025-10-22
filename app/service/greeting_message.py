from datetime import datetime

def get_greeting():
    """Return greeting message based on current hour."""
    hour = datetime.now().hour
    periods = [(range(5,12), 'Доброе утро☀️'),
                (range(12,18), 'Добрый день🌤️'),
                (range(18,24), 'Добрый вечер🌙'),
                (range(0,5), 'Добрый вечер🌙'),]
    greeting = "Привет"
    for period, greeting_text in periods:
        if hour in period:
            greeting = greeting_text
            break
    return greeting   
   