import math
import logging
from django import template

register = template.Library()

# Set up logging
# logger = logging.getLogger(__name__)

@register.filter
def years_to_double(stock):
    """
    Calculate the number of years to double the investment using
    the dividends yield.
    """
    try:
        if not hasattr(stock, 'cash_amount') or not hasattr(stock, 'closep'):
            # logger.error(f'Missing attributes: cash_amount or closep on {stock}')
            return "N/A Error"

        dyield = float(stock.cash_amount) / float(stock.closep)
        # logger.debug(f'Dividend Yield: {dyield}')

        if dyield == 0:
            return "N/A == 0"

        years_to_double = math.log(2) / math.log(1 + dyield)
        return round(years_to_double, 2)  # Rounded to 2 decimal places for readability

    except ZeroDivisionError as e:
        # logger.error(f'ZeroDivisionError: {e}')
        return "N/A ZeroDiv"
    except AttributeError as e:
        # logger.error(f'AttributeError: {e}')
        return "N/A AttrError"
    except TypeError as e:
        # logger.error(f'TypeError: {e}')
        return "N/A TypeError"
    except Exception as e:
        # logger.error(f'Unexpected error: {e}')
        return "N/A Error"
