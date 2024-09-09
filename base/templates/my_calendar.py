import my_calendar
from datetime import datetime

def generar_calendario(mes=None, año=None):
    # Si no se proporciona un mes o año, se usa el mes y año actuales
    if mes is None or año is None:
        ahora = datetime.now()
        mes = ahora.month
        año = ahora.year

    # Crear el calendario HTML
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    calendario_html = cal.formatmonth(año, mes)
    return calendario_html
