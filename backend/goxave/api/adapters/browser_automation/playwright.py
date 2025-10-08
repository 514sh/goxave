from playwright.async_api._context_manager import (
    PlaywrightContextManager as AsyncPlaywrightContextManager,
)
from playwright.sync_api._context_manager import PlaywrightContextManager


class SyncPlaywright(PlaywrightContextManager):
    pass


class AsyncPlaywright(AsyncPlaywrightContextManager):
    pass
