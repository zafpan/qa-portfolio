from pages.login_page import LoginPage  # import the LoginPage class
from pages.secure_area_page import SecureAreaPage  # import the SecureAreaPage class


def test_invalid_login_wrong_password(driver, base_url, valid_credentials):
    """
    Negative path:
    - Open the login page and verify is loaded
    - Enter valid username but wrong password
    - Expect an error flash message and to stay on /login
    """

    login_page = LoginPage(driver, base_url)  # create LoginPage object
    login_page.open()

    # Assertion:
    #   Verify the login page is loaded
    assert login_page.is_loaded(), "Login page did not load properly."

    username, _ = valid_credentials  # get valid credentials
    login_page.login(username, "WrongPassword123")  # perform login action with wrong password

    # Assertion:
    #   After failed login, should remain on login page
    assert login_page.is_at(), "Did not remain on login page after invalid login."

    flash_text = login_page.get_flash_text()  # get flash message text

    # Assertion:
    #   Error message should contain expected text
    msg = flash_text.lower()
    assert "password is invalid" in msg, f"Unexpected flash: {flash_text!r}"


def test_empty_username_shows_error(driver, base_url, valid_credentials):
    """
    Validation:
    - Open the login page and verify is loaded
    - Empty username, valid password
    - Expect error flash and still on /login
    """

    login_page = LoginPage(driver, base_url)  # create LoginPage object
    login_page.open()

    # Assertion:
    #   Verify the login page is loaded
    assert login_page.is_loaded(), "Login page did not load properly."

    _, password = valid_credentials  # get valid credentials
    login_page.login("", password)  # perform login action with empty username

    # Assertion:
    #   After failed login, should remain on login page
    assert login_page.is_at(), "Did not remain on login page after invalid login."

    flash_text = login_page.get_flash_text()  # get flash message text

    # Assertion:
    #   Error message should contain expected text
    assert "username is invalid" in flash_text.lower(), f"Unexpected flash: {flash_text!r}"


def test_empty_password_shows_error(driver, base_url, valid_credentials):
    """
    Validation:
    - Open the login page and verify is loaded
    - Valid username, empty password
    - Expect error flash and still on /login
    """

    login_page = LoginPage(driver, base_url)  # create LoginPage object
    login_page.open()

    # Assertion:
    #   Verify the login page is loaded
    assert login_page.is_loaded(), "Login page did not load properly."

    username, _ = valid_credentials  # get valid credentials
    login_page.login(username, "")  # perform login action with empty password

    # Assertion:
    #   After failed login, should remain on login page
    assert login_page.is_at(), "Did not remain on login page after invalid login."

    flash_text = login_page.get_flash_text()  # get flash message text

    # Assertion:
    #   Error message should contain expected text
    assert "password is invalid" in flash_text.lower(), f"Unexpected flash: {flash_text!r}"


def test_unusual_input_shows_error(driver, base_url):
    """
    Negative / robustness:
    - Open the login page and verify is loaded
    - Use unusual or long strings for username/password
    - Expect invalid login message and stay on /login
    """

    login_page = LoginPage(driver, base_url)  # create LoginPage object
    login_page.open()

    # Assertion:
    #   Verify the login page is loaded
    assert login_page.is_loaded(), "Login page did not load properly."

    # Perform login action with unusual inputs
    weird_username = "<script>alert('xss')</script>"  # unusual / special-character input
    weird_password = "A" * 500  # very long password
    login_page.login(weird_username, weird_password)  # perform login action

    # Assertion:
    #   After failed login, should remain on login page
    assert login_page.is_at(), "Did not remain on login page after invalid login."

    flash_text = login_page.get_flash_text()  # get flash message text

    # Assertion:
    #   Error message should contain expected text
    assert "invalid" in flash_text.lower(), f"Unexpected flash: {flash_text!r}"


def test_access_secure_area_without_login(driver, base_url):
    """
    Negative / robustness:
    - Open the secure page URL directly without logging in
    - Expect to be redirected to login page with error message
    """

    login_page = LoginPage(driver, base_url)  # create LoginPage object
    secure_page = SecureAreaPage(driver, base_url)  # create SecureAreaPage object
    secure_page.open()  # navigate to secure area page directly

    # Assertion:
    #   Verify we are redirected to login page
    assert login_page.is_loaded(), "Did not redirect to login page when accessing secure area without login."

    flash_text = login_page.get_flash_text()  # get flash message text

    # Assertion:
    #   Error message should contain expected text
    msg = flash_text.lower()
    assert ("must login" in msg) or ("must log in" in msg), f"Unexpected flash: {flash_text!r}"
