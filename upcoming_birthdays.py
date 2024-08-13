from datetime import datetime, timedelta


def get_upcoming_birthdays(address_book):
    today = datetime.today().date()
    current_week_number = today.isocalendar()[1]
    current_day_number = today.timetuple().tm_yday
    weeks_days_list = [
        "Понеділок",
        "Вівторок",
        "Середа",
        "Четвер",
        "П'ятниця",
        "Минулі вихідні",
        "Минулі вихідні"
    ]

    this_week_birthdays = {}
    next_week_birthdays = {}

    def set_birthday(week_day, user_name, is_current_week):
        if is_current_week:
            if weeks_days_list[week_day] in this_week_birthdays:
                this_week_birthdays[weeks_days_list[week_day]] = (this_week_birthdays[weeks_days_list[week_day]]
                                                                  + ", "
                                                                  + user_name)
            else:
                this_week_birthdays[weeks_days_list[week_day]] = user_name
        else:
            if weeks_days_list[week_day] in next_week_birthdays:
                next_week_birthdays[weeks_days_list[week_day]] = (next_week_birthdays[weeks_days_list[week_day]]
                                                                  + ", "
                                                                  + user_name)
            else:
                next_week_birthdays[weeks_days_list[week_day]] = user_name

    for user in address_book.data.values():
        if user.birthday:
            birthday = user.birthday.value.date()  # Extract the date from Birthday object
            birthday_week_number = birthday.isocalendar()[1]
            birthday_day_number = birthday.timetuple().tm_yday

            if birthday_week_number == current_week_number and current_day_number <= birthday_day_number:
                if birthday.weekday() <= 4:
                    set_birthday(birthday.weekday(), user.name.value, True)
                else:
                    set_birthday(birthday.weekday(), user.name.value, False)
            elif (birthday_week_number - 1 == current_week_number
                  and (current_day_number + 6) >= birthday_day_number
                  and birthday.weekday() <= 4):
                set_birthday(birthday.weekday(), user.name.value, False)

    this_week_birthdays_info = f"Список привітань на цьому тижні: {this_week_birthdays}" \
        if len(this_week_birthdays) \
        else "На цьому тижні немає привітань."
    next_week_birthdays_info = f"Список привітань на наступному тижні: {next_week_birthdays}" \
        if len(next_week_birthdays) \
        else "На наступному тижні немає привітань."

    return this_week_birthdays_info, next_week_birthdays_info
