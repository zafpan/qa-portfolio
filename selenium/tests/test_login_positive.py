from pages.login_page import LoginPage  # import the LoginPage class
from pages.secure_area_page import SecureAreaPage  # import the SecureAreaPage class


def test_valid_login(driver, base_url, valid_credentials):
    """
    Basic positive login test:
    - Open the login page
    - Verify page is loaded
    - Login with valid username/password
    - Verify secure area page is loaded
    - Verify success message starts with expected text
    """

    login_page = LoginPage(driver, base_url)  # create LoginPage object
    login_page.open()

    # Assertion:
    #   Verify the login page is loaded
    assert login_page.is_loaded(), "Login page did not load properly."

    username, password = valid_credentials  # get valid credentials
    login_page.login(username, password)  # perform login action
    secure_page = SecureAreaPage(driver, base_url)  # create SecureAreaPage object

    # Assertion:
    #   Verify the secure area page is loaded
    assert secure_page.is_loaded(), "Secure area page did not load after login."

    flash_text = secure_page.get_flash_text()  # get flash message text

    # Assertion:
    #   Success message should start with expected text
    assert flash_text.startswith("You logged into a secure area!"), f"Unexpected flash: {flash_text!r}"


def test_logout_redirects_to_login(driver, base_url, valid_credentials):
    """
    Navigation:
    - Open the login page and verify is loaded
    - Login successfully
    - Verify secure area page is loaded
    - Click Logout
    - Verify login page is loaded - after redirect
    - Verify logout message starts with expected text
    """

    login_page = LoginPage(driver, base_url)  # create LoginPage object
    login_page.open()

    # Assertion:
    #   Verify the login page is loaded
    assert login_page.is_loaded(), "Login page did not load properly."

    username, password = valid_credentials  # get valid credentials
    login_page.login(username, password)  # perform login action

    secure_page = SecureAreaPage(driver, base_url)  # create SecureAreaPage object

    # Assertion:
    #   Verify the secure area page is loaded
    assert secure_page.is_loaded(), "Secure area page did not load after login."

    secure_page.click_logout()  # perform logout action

    #
    # Redirects back to login page
    #
    login_page = LoginPage(driver, base_url)  # create new LoginPage object

    # Assertion:
    #   Verify the login page is loaded
    #   - use a longer timeout to account for redirect delay
    assert login_page.is_loaded(timeout=15), "Login page did not load after logout."

    flash_text = login_page.get_flash_text()  # get flash message text

    # Assertion:
    #   Logout message should start with expected text
    assert flash_text.startswith("You logged out of the secure area!"), f"Unexpected flash: {flash_text!r}"
