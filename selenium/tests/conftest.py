import datetime  # for timestamping screenshots
import os  # for filesystem operations
import pytest  # for pytest fixtures and hooks
import re  # for sanitizing filenames
import logging  # for logging

from dotenv import load_dotenv  # for loading .env files
from selenium import webdriver  # for Selenium WebDriver
from selenium.webdriver.chrome.options import Options  # for Chrome options
from selenium.webdriver.chrome.service import Service  # for Chrome service
from webdriver_manager.chrome import ChromeDriverManager  # for managing ChromeDriver


# Constants for valid login credentials
LOGIN_USERNAME = "tomsmith"
LOGIN_PASSWORD = "SuperSecretPassword!"


load_dotenv()  # load environment variables from .env file if present
logger = logging.getLogger(__name__)  # set up module-level logger


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://the-internet.herokuapp.com").rstrip("/")


@pytest.fixture(scope="session")
def valid_credentials() -> tuple[str, str]:
    return LOGIN_USERNAME, LOGIN_PASSWORD


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> webdriver.Chrome:
    """
    Pytest fixture to provide a Selenium Chrome WebDriver instance.

    - Setup: start Chrome
    - Teardown: quit Chrome after the test

    Any test function that takes `driver` as a parameter will
    automatically receive this WebDriver instance.

    We also attach the driver to the test `request.node` so that
    hooks (e.g. for screenshots on failure) can access it.

    Parameters
    ----------
    request : pytest.FixtureRequest
        The pytest fixture request object.
    """

    chrome_options = Options()

    # Optionally run in headless mode based on environment variable
    headless = os.getenv("HEADLESS", "false").lower() in ("1", "true", "yes") # check env var
    if headless:
        chrome_options.add_argument("--headless=new")  # enable headless mode
        chrome_options.add_argument("--disable-gpu")  # disable GPU
        chrome_options.add_argument("--no-sandbox")  # disable sandbox (mainly for Linux CI containers)
        chrome_options.add_argument("--disable-dev-shm-usage")  # disable /dev/shm usage (mainly for Linux CI containers)

    chrome_options.add_argument("--window-size=1920,1080") # set window size

    # Create a Chrome WebDriver instance (browser controller)
    # ChromeDriverManager().install() downloads/locates the right driver automatically.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Attach to node for use in pytest hooks
    request.node.driver = driver

    yield driver  # this is where the test runs

    # Teardown code: runs after the test completes (pass or fail)
    logger.info("Closing browser...")
    try:
        driver.quit()  # quit the driver to close the browser
    except Exception:
        logger.exception("Error while quitting the browser")


def _screenshot_path_for_item(item) -> str:
    """
    Build a filesystem path for the screenshot of a given test item.

    The path includes the test module and function names,
    as well as a timestamp to ensure uniqueness.
    e.g. artifacts/screenshots/test_login_negative__test_invalid_login_wrong_password__2025-12-02_12-34-56.png

    Parameters
    ----------
    item : pytest.Item
        The pytest test item for which to build the screenshot path.

    Returns
    -------
    str
        The full filesystem path for the screenshot.
    """

    # Base folder for screenshots
    base_dir = os.path.join("artifacts", "screenshots")
    os.makedirs(base_dir, exist_ok=True)  # ensure directory exists

    # test nodeid looks like: 'tests/test_login_negative.py::test_invalid_login_wrong_password'
    raw_nodeid = item.nodeid
    safe_nodeid = raw_nodeid.replace("::", "__").replace("/", "_").replace("\\", "_").replace(":", "_")  # sanitize for filesystem
    safe_nodeid = re.sub(r"[^a-zA-Z0-9._-]+", "_", safe_nodeid).strip("_")  # further sanitize
    safe_nodeid = safe_nodeid[:150]  # truncate to avoid overly long filenames

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )  # current timestamp

    filename = f"{safe_nodeid}__{timestamp}.png"  # build filename
    return os.path.join(base_dir, filename)  # return full path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    Pytest hook that is called after each test phase (setup/call/teardown).

    We use it to detect test failures and, if a Selenium `driver`
    is attached to the item, capture a screenshot.

    Parameters
    ----------
    item : pytest.Item
        The pytest test item.
    call : pytest.CallInfo
        Information about the test call phase.
    """

    # Run all other hooks to get the report object
    outcome = yield  # continue to other hooks
    report = outcome.get_result()  # get the test report

    # Look only for the 'call' phase (the actual test body),
    # not setup/teardown failures here.
    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)  # get driver if attached

        if driver is not None:
            screenshot_path = _screenshot_path_for_item(
                item
            )  # build path for screenshot
            try:
                driver.save_screenshot(screenshot_path)  # save screenshot to file
                logger.info("[SCREENSHOT] Saved to: %s", screenshot_path)  # log path
            except Exception:
                logger.exception("[SCREENSHOT] Failed to save screenshot")  # log error
