import datetime
from datetime import timedelta
import locale


def get_dates_of_week(week):
    ''' возвращает дни недели заданной недели '''
    d = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    dates = []
    dates_of_week = {
        'weekday': '',
        'month': '',
        'day': '',
        'extraditions': []
    }
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    if week == 0:
        # если неделя не задана то отталкиваемся от текущего дня
        day = datetime.datetime.today()
        week_day = day.strftime('%d %B %Y')
    else:
        pass

    dt = datetime.datetime.strptime(week_day, '%d %B %Y')
    start = dt - timedelta(days=dt.weekday())
    dates_of_week['weekday'] = d[0]
    dates_of_week['month'] = start.strftime('%B')
    dates_of_week['day'] = start.strftime('%d')
    dates.append(dates_of_week)
    for i in range(1, 7):
        dates_of_week = {
            'weekday': '',
            'month': '',
            'day': '',
            'extraditions': []
        }
        end = start + timedelta(days=i)
        dates_of_week['weekday'] = d[i]
        dates_of_week['month'] = end.strftime('%B')
        dates_of_week['day'] = end.strftime('%d')
        dates.append(dates_of_week)

    return dates
