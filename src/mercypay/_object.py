from typing import Any, Dict


class MercyPayObject(dict):  # type: ignore[type-arg]
    """An object of the API: a dict whose fields also read as attributes,
    ``payment.status`` or ``payment["status"]``. A field added later simply appears."""

    def __init__(self, values: Dict[str, Any]) -> None:
        super().__init__({key: _convert(value) for key, value in values.items()})

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None

    def to_dict(self) -> Dict[str, Any]:
        return {key: _unconvert(value) for key, value in self.items()}


def _convert(value: Any) -> Any:
    if isinstance(value, dict):
        return MercyPayObject(value)
    if isinstance(value, list):
        return [_convert(item) for item in value]
    return value


def _unconvert(value: Any) -> Any:
    if isinstance(value, MercyPayObject):
        return value.to_dict()
    if isinstance(value, list):
        return [_unconvert(item) for item in value]
    return value
