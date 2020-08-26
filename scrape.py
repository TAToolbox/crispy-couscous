
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from selenium.webdriver import ChromeOptions
from selenium import webdriver
import json
import time
import datetime
from pathlib import Path
from getpass import getpass


def login(username=None, password=None, browser=None):
    if username is None or password is None:
        username = input("Username: ")
        password = getpass(prompt="Password: ")
    if browser.is_element_present_by_name('username', wait_time=2):
        user_form = browser.find_by_name('username')
        user_form.fill(username)
    if browser.is_element_present_by_name('password', wait_time=2):
        pass_form = browser.find_by_name('password')
        pass_form.fill(password)
    browser.find_by_xpath(
        '//*[@id="root"]/div/div[2]/div/form/div/button').click()


def cleanup(string):
    return string.split(':')[-1].strip()


def scrape_details(browser, append_grader=True):

    return_list = []
    if browser.is_element_present_by_xpath('/html/body/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/a[2]', wait_time=2):
        links = list(dict.fromkeys([link['href']
                                    for link in browser.links.find_by_partial_href("/submission")]))
        print(f"Getting reports for {len(links)} submissions")
        for link in links:
            if browser.is_element_present_by_xpath('/html/body/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/a[2]', wait_time=2):
                grade_dict = {}
                current_url = link

                element = browser.links.find_by_partial_href(
                    current_url.split('/submission')[-1]).last
                element.click()

                if browser.is_element_present_by_tag('textarea'):
                    grade_dict['assignment'] = browser.find_by_xpath(
                        '//*[@id="root"]/div/div[2]/div/div/div/div/div[1]/div[1]/div').text
                    grade_dict['comments'] = browser.find_by_tag(
                        'textarea').value
                    grade_dict['grade'] = browser.find_by_xpath(
                        '/html/body/div/div/div[2]/div/div/div/div/div[4]/div/div[1]/div[2]/div[1]').text
                    grade_dict['submissionUrl'] = current_url
                    grade_dict['grader'] = cleanup(browser.find_by_xpath(
                        '//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div[2]/span').text)
                    grade_dict['dateSubmitted'] = cleanup(browser.find_by_xpath(
                        '//*[@id="root"]/div/div[2]/div/div/div/div/div[3]/div/div[1]/p[2]').text)
                    grade_dict['dateDue'] = cleanup(browser.find_by_xpath(
                        '//*[@id="root"]/div/div[2]/div/div/div/div/div[3]/div/div[1]/p[3]').text)
                    grade_dict['student'] = cleanup(browser.find_by_xpath(
                        '//*[@id="root"]/div/div[2]/div/div/div/div/div[3]/div/div[2]/p[1]').text)
                    grade_dict['studentLinks'] = {_link.text.split('.COM')[0].replace('.', ' ').title().replace(' ', ''): _link['href'] for _link in browser.find_by_xpath(
                        '//*[@id="root"]/div/div[2]/div/div/div/div').find_by_css('.grey')}
                    grade_dict['plagiarism'] = bool(browser.find_by_xpath(
                        '//*[@id="root"]/div/div[2]/div/div/div/div/div[4]/div/div[2]/div/input').checked)

                    if append_grader:
                        fill_text = grade_dict['comments'] + \
                            f'\n\n--Graded By: {grade_dict["grader"]}'
                        browser.find_by_tag('textarea').fill(fill_text)

                    print(
                        f"{current_url.split('submission')[-1]} Stored", end='.......\r')

                    ######################################
                    #     Add additional conditions      #
                    #        for Approval here           #
                    ######################################

                    if grade_dict['grade'][0] == 'A' and not grade_dict['plagiarism']:
                        browser.find_by_xpath(
                            '//*[@id="root"]/div/div[2]/div/div/div/div/div[4]/div/div[3]/button').click()
                        print(f"Approved {grade_dict['student']}", end="\r")
                        grade_dict['approved'] = True
                    else:
                        grade_dict['approved'] = False

                    return_list.append(grade_dict)
                    browser.back()
    print(f'Completed report for {len(return_list)} submissions')
    return return_list


def approve(username, password, headless=True, **kwargs):

    options = ChromeOptions()

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # Sometimes headless works, sometimes it doesn't
    # it has something to do with the position of the login button in the headless browser
    browser = Browser('chrome', headless=headless, options=options)

    now = datetime.datetime.now().strftime('%m_%d_%y')
    print(now)
    print("Browser Loading......", end='\r')

    browser.visit('https://grading.bootcampspot.com/')

    # Put your own login details here
    print("Logging in", end='........\r')
    login(username, password, browser)
    results = scrape_details(browser, **kwargs)
    browser.quit()

    for idx, result in enumerate(results):
        assignment = result['assignment'].split('.')[1].split('Homework')[
            0].strip().replace(' ', '_')
        report_dir = Path(f'./reports/{assignment}')
        if not report_dir.exists():
            report_dir.mkdir(parents=True, exist_ok=False)
        report_path = report_dir.joinpath(f'{now}.json')
        if report_path.exists():
            with report_path.open(mode='r+', encoding='utf-8') as f:
                data = json.load(f)
                if not result in data:
                    data.append(result)
                    f.seek(0)
                    json.dump(data, f)
                    f.close()
        else:
            report_path.touch(exist_ok=False)
            with report_path.open(mode='w+', encoding='utf-8') as f:
                json.dump([result], f)
