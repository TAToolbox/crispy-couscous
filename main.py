from scrape import approve
from pathlib import Path

if __name__ == "__main__":
    try:
        from config import login_details
        approve(login_details['username'],
                login_details['password'], headless=False)
    except:
        approve(headless=False)
