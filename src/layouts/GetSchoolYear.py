from datetime import date

def get_current_school_year():
    today = date.today()
    year = today.year

    # Philippine school year starts June (6)
    if today.month >= 6:
        return f"{year}-{year+1}"
    else:
        return f"{year-1}-{year}"