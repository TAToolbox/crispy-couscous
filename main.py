from scrape import approve
from config import login_details
from pathlib import Path

if __name__ == "__main__":
    approve(login_details['username'],
            login_details['password'], headless=False, append_grader=True)
