def set_default(default_dict: dict, result_dict: dict):
    """Sets default values for a dictionary recursively.

    :param default_dict: The template dictionary to use to set values
    :param result_dict: The dictionary to load the template values into
    
    :rtype: dict
    """

    # Iterate through default values
    for tag in default_dict:

        # If the tag does not exist in the result dictionary, add it
        if tag not in result_dict:
            result_dict[tag] = default_dict[tag]
        
        # Tag exists in guild dict, see if tag is a dictionary
        else:
            if type(result_dict[tag]) == dict:
                result_dict[tag] = set_default(default_dict[tag], result_dict[tag])
    
    return result_dict

def datetime_to_dict(date_time) -> dict:
    """Turns a datetime.datetime object into a JSON object
    that keeps track of the year, month, day, hour, minute, and second

    :param date_time: A datetime object to convert into a JSON object
    :returns: The datetime object as JSON object
    """

    return {
        "year": date_time.year,
        "month": date_time.month,
        "day": date_time.day,
        "hour": date_time.hour,
        "minute": date_time.minute,
        "second": date_time.second
    }

def datetime_to_string(date_time, *, short: bool=False):
    """Turns a datetime into a readable string.

    :param date_time: The datetime object to convert
    :param short: Whether or not to get a shortened version of the datetime in the MM/DD/YYYY format. (Defaults to False)
    """

    if short:
        return "{}/{}/{}".format(
            date_time.month,
            date_time.day,
            date_time.year
        )
    
    else:

        # Get the weekday
        weekday = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday",
            "Saturday", "Sunday"
        ][date_time.weekday()]

        month = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ][date_time.month - 1]

        # Get the day, year, time (AM or PM)
        day = date_time.day
        year = date_time.year
        hour = date_time.hour
        am = True
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12
            am = False
        minute = date_time.minute
        if minute < 10:
            minute = "0" + str(minute)

        return "{}, {} {}, {} {}:{} {}".format(
            weekday, month, day, year, 
            hour, minute, "AM" if am else "PM"
        )
