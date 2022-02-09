import typing

from babel import support

from app.config import general

settings = general.get_settings()


translations = support.Translations.load("locale", settings.LOCALES)

gettext = translations.gettext


class LazyString:  # pragma: no cover
    """
    Implement lazy evaluation of the string.

    Taken from the flask-babel library.
    """

    def __init__(
        self,
        func: typing.Callable[..., typing.Any],
        *args: typing.Any,
        **kwargs: typing.Any,
    ):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __getattr__(self, attr: str) -> typing.Any:
        if attr == "__setstate__":
            raise AttributeError(attr)

        string = str(self)
        if hasattr(string, attr):
            return getattr(string, attr)

        raise AttributeError(attr)

    def __repr__(self) -> str:
        return f"l'{self}'"

    def __str__(self) -> str:
        return str(self._func(*self._args, **self._kwargs))

    def __len__(self) -> int:
        return len(str(self))

    def __getitem__(self, key: int) -> str:
        return str(self)[key]

    def __iter__(self) -> typing.Iterator[str]:
        return iter(str(self))

    def __contains__(self, item: str) -> bool:
        return item in str(self)

    def __add__(self, other: str) -> str:
        return str(self) + other

    def __radd__(self, other: str) -> str:
        return other + str(self)

    def __mul__(self, other: int) -> str:
        return str(self) * other

    def __rmul__(self, other: int) -> str:
        return other * str(self)

    def __lt__(self, other: str) -> bool:
        return str(self) < other

    def __le__(self, other: str) -> bool:
        return str(self) <= other

    def __eq__(self, other: object) -> bool:
        return str(self) == other

    def __ne__(self, other: object) -> bool:
        return str(self) != other

    def __gt__(self, other: str) -> bool:
        return str(self) > other

    def __ge__(self, other: str) -> bool:
        return str(self) >= other

    def __html__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __mod__(self, other: typing.Any) -> str:
        return str(self) % other

    def __rmod__(self, other: str) -> str:
        return other + str(self)


def gettext_lazy(string: str, **kwargs: typing.Any) -> LazyString:
    return LazyString(gettext, string, **kwargs)
