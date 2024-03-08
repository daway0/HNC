import jdatetime
import pytz


def beautify_string_cut(string: str, max_len=35) -> str:
    if len(string) < max_len:
        return string
    return string[: max_len - 3] + "..."


def put_comma_for_numbers(number: int) -> str:
    """mainly use for cost
    1200000 toman -> 1,200,000 toman
    """
    reversed_number_list = list(reversed(list(str(number))))
    c = 0
    number_with_comma = []
    for num in reversed_number_list:
        if c % 3 == 0 and c > 0:
            number_with_comma.append(",")
        number_with_comma.append(num)
        c += 1

    return "".join(list(reversed(number_with_comma)))


def localnow() -> jdatetime.datetime:
    utc_now = jdatetime.datetime.now(tz=pytz.utc)
    local_timezone = pytz.timezone("Asia/Tehran")
    return utc_now.astimezone(local_timezone)


def current_date() -> tuple[int, int, int]:
    """Returning current date"""
    now = localnow()
    return now.year, now.month, now.day


def current_date_str() -> str:
    """Returning current date str"""
    now = localnow()
    return f"{now.year}/{now.month}/{now.day}"


def get_multiple_cleaned_data(cd: dict, fields: list[str]) -> tuple:
    r = []
    for field_name in fields:
        if not isinstance(field_name, str):
            raise TypeError("Field name must be a string")

        r.append(cd.get(field_name, None))
    return tuple(r)


def map_to_model_data(cleaned_data: dict, map_fields: list[tuple[str, str]]) -> dict:
    """extract model data from cleaned data
    it actually acts like a mapper
    """

    extract = {}
    for fields_pair in map_fields:
        # from form data to model data
        from_field = fields_pair[0]
        try:
            to_field = fields_pair[1]
            extract[to_field] = cleaned_data.get(from_field, None)
        except IndexError:
            # from_field equals to to_field
            # user knows that the form field name is the same as model field
            # name, and he/she didn't pass the destination
            extract[from_field] = cleaned_data.get(from_field, None)

    return extract
