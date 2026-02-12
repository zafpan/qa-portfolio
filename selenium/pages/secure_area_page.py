from __future__ import annotations  # treat type hints as strings instead of active objects (Python 3.7+)

from selenium.webdriver.common.by import By  # locator strategies e.g. By.ID, By.CSS_SELECTOR
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
    element_to_be_clickable,
)  # expected conditions for waits

from typing import TYPE_CHECKING  # for type hinting
from urllib.parse import urlparse  # for URL parsing
from pages.base_page import BasePage  # import BasePage

# Type checking imports - only imported during type checking, not at runtime.
if TYPE_CHECKING:
    from selenium.webdriver.support.ui import WebDriverWait


class SecureAreaPage(BasePage):
    """
    Page Object for the secure area after successful login.

    Responsibilities:
    - Represent the '/secure' page
    - Provide logout action
    - Expose helpers related to this page

    NOTE: It does NOT assert anything itself; assertions stay in the tests.
    """

    # URL path for the secure area page
    PATH = "/secure"

    # Locators as class attributes (tuple: (By, locator_string))
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a[href='/logout']")  # for Logout button


    def wait_until_loaded(self, wait: WebDriverWait | None = None) -> None:
        """
        Helper to wait until the secure area page is fully loaded.

        NOTE: Doing a path equality check, but also wait for
        a specific element that only exists on this page.

        Parameters
        ----------
        wait : WebDriverWait | None, optional
            An optional WebDriverWait instance to use for waiting.
        """

        wait = wait or self.wait # use provided wait or default
        wait.until(lambda d: urlparse(d.current_url).path.rstrip("/") == self.PATH)  # wait until URL path equals /secure
        wait.until(presence_of_element_located(self.LOGOUT_BUTTON))  # ensure logout button is present



    def click_logout(self) -> None:
        """Helper to click the Logout button."""

        # Locate Logout button and wait until clickable
        logout_button = self.wait.until(element_to_be_clickable(self.LOGOUT_BUTTON))  # for Logout button
        logout_button.click()  # click the button
