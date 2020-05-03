"""
Project for Week 4 of "Python Programming Essentials".
Collection of functions to process dates.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""
import datetime
def days_in_month(year, month):
    """
    Inputs:
      year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
              representing the year
      month - an integer between 1 and 12 representing the month

    Returns:
      The number of days in the input month.
    """
    if (month == 12):
        number_of_days = datetime.date(year, month, 1) - datetime.date(year, month - 1, 1)
        number_of_days = number_of_days.days + 1
        return number_of_days
    else:
        number_of_days = datetime.date(year, month + 1, 1) - datetime.date(year, month, 1)
        return number_of_days.days

def is_valid_date(year, month, day):
    """
    Inputs:
      year  - an integer representing the year
      month - an integer representing the month
      day   - an integer representing the day

    Returns:
      True if year-month-day is a valid date and
      False otherwise
    """
    if datetime.MINYEAR <= year <= datetime.MAXYEAR:
        if month == 12:
            number_of_days = datetime.date(year, month, 1) - datetime.date(year, month - 1, 1)
            number_of_days = number_of_days.days + 1
        elif 1 <= month <= 12:
            number_of_days = datetime.date(year, month + 1, 1) - datetime.date(year, month, 1)
            number_of_days = number_of_days.days
        if 1 <= month <= 12:
            if 1 <= day <= number_of_days:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def days_between(year1, month1, day1, year2, month2, day2):
    """
    Inputs:
      year1  - an integer representing the year of the first date
      month1 - an integer representing the month of the first date
      day1   - an integer representing the day of the first date
      year2  - an integer representing the year of the second date
      month2 - an integer representing the month of the second date
      day2   - an integer representing the day of the second date

    Returns:
      The number of days from the first date to the second date.
      Returns 0 if either date is invalid or the second date is
      before the first date.
    """
    if is_valid_date(year1, month1, day1):
        if is_valid_date(year2, month2, day2):
            if datetime.date(year1, month1, day1) < datetime.date(year2, month2, day2):
                first_month = datetime.date(year2, month2, day2)
                second_month = datetime.date(year1, month1, day1)
                number_of_days = first_month - second_month
                return number_of_days.days
            else:
                return 0
        else:
            return 0
    else:
        return 0

def age_in_days(year, month, day):
    """
    Inputs:
      year  - an integer representing the birthday year
      month - an integer representing the birthday month
      day   - an integer representing the birthday day

    Returns:
      The age of a person with the input birthday as of today.
      Returns 0 if the input date is invalid or if the input
      date is in the future.
    """
    year2 = datetime.date.today().year
    month2 = datetime.date.today().month
    day2 = datetime.date.today().day
    if is_valid_date(year, month, day):
        if datetime.date.today() > datetime.date(year, month, day):
            return days_between(year, month, day, year2, month2, day2)
        else:
            return 0
    else:
        return 0


