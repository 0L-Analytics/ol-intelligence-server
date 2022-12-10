# doc reference: https://flask-restx.readthedocs.io/en/latest/_modules/flask_restx/inputs.html
import re

ol_address_regex = re.compile(
    r"[a-fA-F0-9]{32}$",
    re.IGNORECASE,
)


def ol_address(value):
    """Validate an 0L address"""
    try:
        match = ol_address_regex.match(value)
        if match:
            return value
    except Exception as e:
        pass
    raise ValueError("{0} is not a valid 0L address".format(value))


ol_address.__schema__ = {"type": "string", "format": "ol_address"}


class regex(object):
    """
    Validate a string based on a regular expression.

    Example::

        parser = reqparse.RequestParser()
        parser.add_argument('example', type=inputs.regex('^[0-9]+$'))

    Input to the ``example`` argument will be rejected if it contains anything
    but numbers.

    :param str pattern: The regular expression the input must match
    """

    def __init__(self, pattern):
        self.pattern = pattern
        self.re = re.compile(pattern)

    def __call__(self, value):
        if not self.re.search(value):
            message = 'Value does not match pattern: "{0}"'.format(self.pattern)
            raise ValueError(message)
        return value

    def __deepcopy__(self, memo):
        return regex(self.pattern)

    @property
    def __schema__(self):
        return {
            "type": "string",
            "pattern": self.pattern,
        }


def _get_integer(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError("{0} is not a valid integer".format(value))


def natural(value, argument="argument"):
    """Restrict input type to the natural numbers (0, 1, 2, 3...)"""
    value = _get_integer(value)
    if value < 0:
        msg = "Invalid {arg}: {value}. {arg} must be a non-negative integer"
        raise ValueError(msg.format(arg=argument, value=value))
    return value


natural.__schema__ = {"type": "integer", "minimum": 0}


def positive(value, argument="argument"):
    """Restrict input type to the positive integers (1, 2, 3...)"""
    value = _get_integer(value)
    if value < 1:
        msg = "Invalid {arg}: {value}. {arg} must be a positive integer or zero"
        raise ValueError(msg.format(arg=argument, value=value))
    return value


positive.__schema__ = {"type": "integer", "minimum": 0, "exclusiveMinimum": True}


class int_range(object):
    """Restrict input to an integer in a range (inclusive)"""

    def __init__(self, low, high, argument="argument"):
        self.low = low
        self.high = high
        self.argument = argument

    def __call__(self, value):
        value = _get_integer(value)
        if value < self.low or value > self.high:
            msg = "Invalid {arg}: {val}. {arg} must be within the range {lo} - {hi}"
            raise ValueError(
                msg.format(arg=self.argument, val=value, lo=self.low, hi=self.high)
            )
        return value

    @property
    def __schema__(self):
        return {
            "type": "integer",
            "minimum": self.low,
            "maximum": self.high,
        }
