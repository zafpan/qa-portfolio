from __future__ import annotations  # treat type hints as strings instead of active objects (Python 3.7+)

from selenium.webdriver.common.by import By  # locator strategies e.g. By.ID, By.CSS_SELECTOR
from selenium.webdriver.support.expected_conditions import visibility_of_element_located  # expected conditions for waits
from selenium.webdriver.support.ui import WebDriverWait  # explicit wait class
from selenium.common.exceptions import TimeoutException  # for handling timeouts

from typing import TYPE_CHECKING  # for type hinting
from urllib.parse import urlparse  # for URL parsing

# Type checking imports - only imported during type checking, not at runtime.
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement


class BasePage:
    """
    Base Page Object class providing common functionality for all pages.

    Responsibilities:
    - Store WebDriver and WebDriverWait instances
    - Provide common helpers (e.g. open page, get flash message)

    NOTE: It does NOT assert anything itself; assertions stay in the tests.
    """

    PATH: str = "/"  # override in subclasses

    # Locators as class attributes (tuple: (By, locator_string))
    FLASH_MESSAGE = (By.CSS_SELECTOR, "div.flash")  # for flash message (success or error)


    def __init__(self, driver: WebDriver, base_url: str | None = None, timeout: int = 10) -> None:
        """
        Initialize with a Selenium WebDriver instance, optional timeout for waits,
        and optional base URL from fixture.

        Parameters
        ----------
        driver : WebDriver
            Selenium WebDriver instance to interact with the browser.
        base_url : str | None, optional
            The base URL of the application under test.
        timeout : int, optional
            Timeout in seconds for explicit waits (default is 10).
        """

        self.driver = driver  # Selenium WebDriver instance
        self.wait = WebDriverWait(driver, timeout)  # explicit wait instance

        self.base_url = base_url.rstrip("/") if base_url else None # base URL from fixture


    @property
    def url(self) -> str:
        """
        A read-only property that builds and returns the full URL of the page.

        Returns
        -------
        str
            The full URL of the page.
        """

        if not self.base_url:
            raise ValueError(
                f"{self.__class__.__name__} requires base_url to build URL (PATH={self.PATH!r})"
            )

        return f"{self.base_url}{self.PATH}"


    def wait_until_loaded(self, wait: WebDriverWait | None = None) -> None:
        """
        Page-specific helper to wait until the page is fully loaded.

        NOTE: Must be implemented in subclasses.

        Parameters
        ----------
        wait : WebDriverWait | None, optional
            An optional WebDriverWait instance to use for waiting.
        """

        raise NotImplementedError(
            f"{self.__class__.__name__} must implement wait_until_loaded()"
        )


    def is_loaded(self, timeout: int | None = None) -> bool:
        """
        Helper to verify if the page is currently loaded.

        NOTE: Relies on page-specific `wait_until_loaded()`.

        Parameters
        ----------
        timeout : int | None, optional
            An optional timeout in seconds for waiting.

        Returns
        -------
        bool
            True if the page is open, False otherwise.
        """

        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait # use provided wait or default

        try:
            self.wait_until_loaded(wait=wait)
            return True
        except TimeoutException:
            return False


    def is_at(self) -> bool:
        """
        Helper to check if currently on the page based on URL path.

        NOTE: Treats empty path as "/" to handle home page correctly.

        Returns
        -------
        bool
            True if current URL path is equal to the page's PATH, False otherwise.
        """

        path = urlparse(self.driver.current_url).path
        path = path.rstrip("/") or "/"
        return path == self.PATH


    def open(self) -> None:
        """
        Helper to navigate to the page URL.

        NOTE: Requires `base_url`, otherwise ValueError is raised in `url` property.
        """

        self.driver.get(self.url)


    def get_flash_element(self) -> WebElement:
        """
        Helper to wait for and return the flash message element (success or error).

        Returns
        -------
        WebElement
            The flash message WebElement.
        """

        return self.wait.until(visibility_of_element_located(self.FLASH_MESSAGE))


    def get_flash_text(self) -> str:
        """
        Helper to get the flash message text.

        Returns
        -------
        str
            The text content of the flash message.
        """

        raw = self.get_flash_element().text or ""

        # Often formatted like: "You logged into a secure area!\n×"
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        return lines[0] if lines else ""
