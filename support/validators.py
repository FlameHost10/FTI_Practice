def get_month_input():
    while True:
        try:
            month = int(input("Enter month (1-12): "))
            if 1 <= month <= 12:
                return month
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")


def get_day_input(year, month):
    days_in_month = {
        1: 31, 2: 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
        3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31,
        11: 30, 12: 31
    }
    max_day = days_in_month.get(month)

    while True:
        try:
            day = int(input(f"Enter day (1-{max_day}): "))
            if 1 <= day <= max_day:
                return day
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")


def get_hour_input():
    while True:
        try:
            hour = int(input("Enter hour (0-23): "))
            if 0 <= hour <= 23:
                return hour
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")


def get_minute_input():
    while True:
        try:
            minute = int(input("Enter minute (0-59): "))
            if 0 <= minute <= 59:
                return minute
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")


def get_user_choice():
    while True:
        user_choice = input("Would you like to choose day and time manually? Y(es)/N(o): ").strip().upper()
        if user_choice in ['Y', 'N']:
            return user_choice
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
