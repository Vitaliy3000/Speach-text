import json
import logging
from functools import wraps


log = logging.getLogger('')


def message_parse(message):
    return {'user_id': message.from_user.id,
            'message_id': message.message_id,
            'is_bot': message.from_user.is_bot,
            'first_name': message.from_user.first_name,
            'username': message.from_user.username,
            'last_name': message.from_user.last_name,
            'language_code': message.from_user.language_code,
            'date': message.date,
            'text': message.text,
    }


def logger(func):
    @wraps(func)
    def wrapper(message):
        log.info(json.dumps(message_parse(message)))
        result = func(message)
        log.info(result)
        return result
    return wrapper


def trier(func):
    @wraps(func)
    def wrapper(message):
        try:
            return func(message)
        except Exception as e:
            log.error(str(e))
    return wrapper