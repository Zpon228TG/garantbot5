import time

from src.utils.utils import split_words_with_underscore
from sqlalchemy import Column, Integer, String


class SqlalchemySerializerMixin:
    """ Dict from sqlalchemy model. """

    def to_dict(self, include: list | str = '__all__', exclude: list = []) -> dict:
        """
            :param include: Return of certain fields if include != __all__.
                   otherwise all fields will be returned
            :param exclude: Fields to be excluded from the response.
        """
        class_variables_dict = {}

        if exclude:
            for variable in vars(self):
                if not variable.startswith("_") and variable not in exclude:
                    try:
                        class_variables_dict[variable] = vars(self)[variable]
                    except KeyError:
                        ...

        else:
            variables = include if include != '__all__' else vars(self)
            for variable in variables:
                try:
                    if not variable.startswith("_"):
                        class_variables_dict[variable] = vars(self)[variable]
                except KeyError:
                    ...

        return class_variables_dict


class SqlalchemyTableMixin:
    def __init_subclass__(cls, **kwargs):
        setattr(cls, '__tablename__',
                split_words_with_underscore(cls.__name__))
