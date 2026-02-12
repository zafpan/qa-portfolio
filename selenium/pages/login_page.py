from __future__ import annotations  # treat type hints as strings instead of active objects (Python 3.7+)

from selenium.webdriver.common.by import By  # locator strategies e.g. By.ID, By.CSS_SELECTOR
from selenium.webdriver.support.expected_conditions import (
    visibility_of_element_located,
    presence_of_element_located,
    element_to_be_clickable,
)  # expected conditions for waits

from typing import TYPE_CHECKING  # for type hinting
from urllib.parse import urlparse  # for URL parsing
from pages.base_page import BasePage  # import BasePage

# Type checking imports - only imported during type checking, not at runtime.
if TYPE_CHECKING:
    from selenium.webdriver.support.ui import WebDriverWait


class LoginPage(BasePage):
    """
    Page Object for the Internet Herokuapp Login Page.

    Responsibilities:
    - Open the login page
    - Perform login action
    - Expose helpers related to this page

    NOTE: It does NOT assert anything itself; assertions stay in the tests.
    """

    # Path to the login page
    PATH = "/login"

    # Locators as class attributes (tuple: (By, locator_string))
    USERNAME_INPUT = (By.ID, "username")  # for username input field
    PASSWORD_INPUT = (By.ID, "password")  # for password input field
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")  # for Login button


    def wait_until_loaded(self, wait: WebDriverWait | None = None) -> None:
        """
        Helper to wait until the login page is fully loaded.

        NOTE: Doing a path equality check, but also wait for
        a specific element that only exists on this page.

        Parameters
        ----------
        wait : WebDriverWait | None, optional
            An optional WebDriverWait instance to use for waiting.
        """

        wait = wait or self.wait # use provided wait or default
        wait.until(lambda d: urlparse(d.current_url).path.rstrip("/") == self.PATH)  # wait until URL path equals /login
        wait.until(presence_of_element_located(self.USERNAME_INPUT))  # ensure username input is present


    def login(self, username: str, password: str) -> None:
        """
        Helper to perform the login action:
        - fills username & password
        - clicks the Login button

        Parameters
        ----------
        username : str
            The username to enter.
        password : str
            The password to enter.
        """

        # Locate elements and wait until they are interactable
        user = self.wait.until(visibility_of_element_located(self.USERNAME_INPUT))  # for username input
        pwd = self.wait.until(visibility_of_element_located(self.PASSWORD_INPUT))  # for password input
        btn = self.wait.until(element_to_be_clickable(self.LOGIN_BUTTON))  # for Login button

        user.clear()  # clear any pre-filled text
        user.send_keys(username)  # enter username

        pwd.clear()  # clear any pre-filled text
        pwd.send_keys(password)  # enter password

        btn.click()  # click Login button
