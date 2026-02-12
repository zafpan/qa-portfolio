from selenium.webdriver.common.by import By  # locator strategies e.g. By.ID, By.CSS_SELECTOR
from selenium.webdriver.support.expected_conditions import visibility_of_element_located  # expected conditions for waits

from pages.login_page import LoginPage  # import the LoginPage class


def test_footer_elemental_selenium_link_visible(driver, base_url):
    """
    UI/link check:
    - Open the login page and verify is loaded
    - Verify the 'Elemental Selenium' footer link is visible and has a non-empty href.
    """

    login_page = LoginPage(driver, base_url)  # create LoginPage object
    login_page.open()  # navigate to login page

    # Assertion:
    #   Verify the login page is loaded
    assert login_page.is_loaded(), "Login page did not load properly."

    link = login_page.wait.until(
        visibility_of_element_located((By.LINK_TEXT, "Elemental Selenium"))
    )  # wait until the link is visible

    # Assertion:
    #   Link should be visible
    assert link.is_displayed(), "'Elemental Selenium' link is not visible."

    href = link.get_attribute("href")  # get href attribute

    # Assertion:
    #   Link should have a non-empty href attribute
    assert href is not None and href != "", "'Elemental Selenium' link has an empty href attribute."

    # Assertion:
    #   Href should point to the expected domain
    assert "elementalselenium" in href.lower(), f"Unexpected href: {href!r}"
