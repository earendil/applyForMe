import json
import logging as log

import requests

from reedclient.utils import read_file


class ReedJobs(object):
    REED_URL = "www.reed.co.uk/api/1.0/"

    def __init__(self, token=""):
        """
        :param token: Reed API token
        """
        self.token = token
        self.jobs = []

    def get_jobs_listing(self, keywords=None):
        """ Currently if you pass any other parameter to the API, you get a bunch of unrelated jobs...

        :param keywords: A list of case insensitive keywords
        :return: dict of jobs (max of 100 jobs due to API limitations)
        """

        query = f"https://{self.token}:@" + self.REED_URL + "search"

        if keywords:
            parsed_keywords = "+".join(keywords)
            query += "?keywords=" + parsed_keywords

        response = requests.get(query)

        parsed_response = json.loads(response.content)

        log.info(f"{parsed_response['totalResults']} jobs found.")

        self.jobs = parsed_response["results"]

    def filter_relevant_jobs(self, disallowedList=None, maxSalary=None):

        if not self.jobs:
            log.info("No jobs to filter")
            return None

        filtered = []
        for job in self.jobs:
            add = True
            if disallowedList:
                for item in disallowedList:
                    if item.lower() in job["jobTitle"].lower():
                        add = False
                        break

            if maxSalary:
                if job["maximumSalary"]:
                    if not (float(job["maximumSalary"]) > maxSalary):
                        add = False

            if "remote" not in job["jobTitle"].lower() and "london" not in job["locationName"].lower():
                add = False

            if add:
                filtered.append(job)

        self.jobs = filtered


if __name__ == "__main__":

    token = read_file("token")

    words = ["python"]

    dis_title = ["tester"]

    reed = ReedJobs(token)

    reed.get_jobs_listing(keywords=words)

    reed.filter_relevant_jobs(disallowedList=dis_title)

    from pprint import pprint
    for job in reed.jobs:
        pprint(job)
