import time
from os import path
import logging
from datetime import datetime

from selenium.webdriver.firefox.webdriver import WebDriver

from reedclient.api import ReedJobs
from reedclient.utils import read_file


class ApplyForMe(object):

    def __init__(self, keywords, filter_out, maxSalary):
        self._driver = None
        self._api = None
        self.keywords = keywords
        self.filter = filter_out
        self.maxSalary = maxSalary

    def loadPage(self, url):
        self.driver.get(url)

    def signIn(self, username, password):
        self.loadPage("https://www.reed.co.uk/account/signin?returnUrl=%2F#&card=signin")
        time.sleep(5)
        self.driver.find_element_by_id("Credentials_Email").send_keys(username)
        self.driver.find_element_by_id("Credentials_Password").send_keys(password)
        self.driver.find_element_by_id("signin-button").click()

    def quit(self):
        self.driver.quit()

    @property
    def driver(self):
        if not self._driver:
            self._driver = WebDriver(executable_path=f"{path.expanduser('~')}/geckodriver")
        return self._driver

    @property
    def api(self):
        if not self._api:
            self._api = ReedJobs(read_file("token"))
            self._api.get_jobs_listing(self.keywords)
            self._api.filter_relevant_jobs(self.filter, maxSalary=self.maxSalary)
        return self._api

    def apply(self):
        appliedJobs = read_file("jobs")

        latestJobs = ""

        for job in self.api.jobs:

            if str(job["jobId"]) not in appliedJobs:
                self.loadPage(job["jobUrl"])
                time.sleep(5)
                try:
                    self.driver.find_element_by_id("applyButtonSide").click()
                    time.sleep(2)
                    self.driver.find_element_by_id("sendApplicationButtonBottom").click()
                except Exception:
                    logging.warning(f"Unable to apply for {job['jobTitle']} with id {job['jobId']}")
                else:
                    latestJobs += f"{job['jobId']}  {job['jobTitle']}  {job['jobUrl']}\n"

        if latestJobs:
            with open(path.expanduser("~") + "/jobs", "a") as f:
                f.write(latestJobs)
                f.write(f"\n Date applied: {datetime.now().date().isoformat()}\n")


if __name__ == "__main__":

    words = ["python"]

    dis_title = ["tester"]

    test = ApplyForMe(words, dis_title, maxSalary=1)

    test.signIn("your@email.com", read_file("pass"))
    time.sleep(5)
    test.apply()
    test.quit()

