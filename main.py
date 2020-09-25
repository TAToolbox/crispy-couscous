from scrape import approve
from pathlib import Path
from selenium.common.exceptions import WebDriverException

if __name__ == "__main__":
    try:
        from config import login_details
        try:
            approve(login_details['username'],
                    login_details['password'], headless=False)
        except WebDriverException:
            approve(login_details['username'],
                    login_details['password'], headless=False, append_grader=False)

    except ImportError:
        try:
            approve(headless=False)
        except WebDriverException:
            approve(headless=False, append_grader=False)
