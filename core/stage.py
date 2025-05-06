from typing import Union, Callable, Any, List

from aiogram.types import ReplyKeyboardMarkup, \
    InlineKeyboardMarkup


class Stage:
    def __init__(
        self,
        msg: Union[str, Callable[[Any], str]],
        kb: Union[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup],
            Callable[[Any], Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]]
        ]
    ) -> None:
        self._msg = msg if callable(msg) else lambda **_: msg
        self._kb = kb if callable(kb) else lambda **_: kb

    def msg(self, *args, **kwargs) -> str:
        return self._msg(*args, **kwargs)

    def kb(self, *args, **kwargs) -> Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]:
        return self._kb(*args, **kwargs)
