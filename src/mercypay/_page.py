from typing import Any, AsyncIterator, Awaitable, Callable, Dict, Iterator, List, Optional

from ._object import MercyPayObject


class Page:
    """One page of a list, newest first. ``page.data`` is this page; ``page.auto_paging_iter()``
    goes through every page, fetched as you go."""

    def __init__(self, body: Dict[str, Any], fetch: Callable[[Dict[str, Any]], "Page"], params: Dict[str, Any]) -> None:
        self.data: List[MercyPayObject] = [MercyPayObject(row) for row in body.get("data") or []]
        self.has_more: bool = bool(body.get("has_more"))
        self.next_cursor: Optional[str] = body.get("next_cursor")
        self._fetch = fetch
        self._params = params

    def next_page(self) -> Optional["Page"]:
        if not self.has_more or self.next_cursor is None:
            return None
        params = {key: value for key, value in self._params.items() if key != "ending_before"}
        return self._fetch({**params, "starting_after": self.next_cursor})

    def auto_paging_iter(self) -> Iterator[MercyPayObject]:
        page: Optional[Page] = self
        while page is not None:
            yield from page.data
            page = page.next_page()

    def __iter__(self) -> Iterator[MercyPayObject]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)


class AsyncPage:
    """The async twin of Page: ``async for item in page.auto_paging_iter()``."""

    def __init__(self, body: Dict[str, Any], fetch: Callable[[Dict[str, Any]], Awaitable["AsyncPage"]], params: Dict[str, Any]) -> None:
        self.data: List[MercyPayObject] = [MercyPayObject(row) for row in body.get("data") or []]
        self.has_more: bool = bool(body.get("has_more"))
        self.next_cursor: Optional[str] = body.get("next_cursor")
        self._fetch = fetch
        self._params = params

    async def next_page(self) -> Optional["AsyncPage"]:
        if not self.has_more or self.next_cursor is None:
            return None
        params = {key: value for key, value in self._params.items() if key != "ending_before"}
        return await self._fetch({**params, "starting_after": self.next_cursor})

    async def auto_paging_iter(self) -> AsyncIterator[MercyPayObject]:
        page: Optional[AsyncPage] = self
        while page is not None:
            for item in page.data:
                yield item
            page = await page.next_page()

    def __iter__(self) -> Iterator[MercyPayObject]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)
