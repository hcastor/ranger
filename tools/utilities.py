def convert_to_number(value):
    """
    Used to blindly convert any number to correct data type
    '-', '' = None
    1,000 = 1000
    1,000.00 = 1000.00
    1.2M = 1200000.00
    """
    if value == '' or value == '-':
        return None
    stripped_value = value.replace(',', '').strip()
    try:
        return int(stripped_value)
    except ValueError:
        pass
    try:
        return float(stripped_value)
    except ValueError:
        pass
    try:
        powers = {'b': 10 ** 9, 'm': 10 ** 6, 't': 10 ** 12}
        return float(stripped_value[:-1]) * powers[stripped_value[-1].lower()]
    except (KeyError, ValueError):
        pass
    return value


def clean_key(value):
    """
    Used to provide consistent key formats in mongo
    """
    replacements = [
        ('.', ''), ('$', ''), (' ', '_'), (':', ''), ('(', ''),
        (')', '')
    ]
    value = value.lower().strip()
    for replacee, replacer in replacements:
        value = value.replace(replacee, replacer)
    return value
