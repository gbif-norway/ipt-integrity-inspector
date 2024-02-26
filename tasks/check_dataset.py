import luigi
import requests
import json
import datetime
import os

class CheckDataset(luigi.Task):
    dataset_id = luigi.Parameter()


    def send_discord_notification(self, message):
        webhook_url = os.getenv('DISCORD_WEBHOOK')
        data = {"content": message}
        requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

    def run(self):
        # URL for the GBIF ingestion history API endpoint
        api_url = f"https://api.gbif.org/v1/ingestion/history/{self.dataset_id}"

        # Perform the GET request
        response = requests.get(api_url)
        if response.status_code != 200:
            self.send_discord_notification(f"Failed to fetch ingestion history for dataset ID {self.dataset_id}")
            with self.output().open('w') as outfile:
                json.dump({
                    "error": f"Failed to fetch ingestion history for dataset ID {self.dataset_id}"
                }, outfile)
            return

        # Parse the JSON response
        data = response.json()

        # Focus on the latest crawl result
        if data["results"]:
            latest_crawl = data["results"][0]  # The first result is always the latest
            finish_reason = latest_crawl["crawlInfo"]["finishReason"]
            processStateOccurrence = latest_crawl["crawlInfo"]["processStateOccurrence"]
            processStateChecklist = latest_crawl["crawlInfo"]["processStateChecklist"]



            # If the finish reason is acceptable, process as normal
            # Extract necessary details from the latest crawl (customize as needed)
            dataset_key = latest_crawl["datasetKey"]
            crawl_attempt = latest_crawl["attempt"]
            dataset_title = latest_crawl["datasetTitle"]
            registry_url = f'https://registry.gbif.org/dataset/{dataset_key}'
            started_crawling = latest_crawl["crawlInfo"]["startedCrawling"]
            finished_crawling = latest_crawl["crawlInfo"]["finishedCrawling"]

            # Check the finish reason
            if finish_reason not in ["NORMAL", "NOT_MODIFIED"]:

                # Notify with a descriptive message
                self.send_discord_notification(f"Ingestion for dataset ID {self.dataset_id} did not finish normally.\n\
                    Reason: {finish_reason}.\n\
                    Title: {dataset_title}\n\
                    Link: {registry_url}")

            # Check the finish reason
            if processStateOccurrence == "EMPTY" and processStateChecklist == "EMPTY":

                # Notify with a descriptive message
                self.send_discord_notification(f"Ingestion for dataset ID {self.dataset_id} did not finish normally.\n\
                    processStateOccurrence and processStateChecklist are booth EMPTY\n\
                    Reason: {finish_reason}.\n\
                    Title: {dataset_title}\n\
                    Link: {registry_url}\n\
                    processStateOccurrence: {processStateOccurrence}\n\
                    processStateChecklist: {processStateChecklist}")

            # Write these details to an output file or process them as needed
            with self.output().open('w') as outfile:
                json.dump({
                    "datasetKey": dataset_key,
                    "attempt": crawl_attempt,
                    "startedCrawling": started_crawling,
                    "finishedCrawling": finished_crawling,
                    "finishReason": finish_reason
                }, outfile)
        else:
            self.send_discord_notification(f"No crawl data found for dataset ID {self.dataset_id}")
            with self.output().open('w') as outfile:
                json.dump({
                    "error": f"No crawl data found for dataset ID {self.dataset_id}"
                }, outfile)

    def output(self):
        return luigi.LocalTarget(f'/tmp/{datetime.datetime.now().date()}_crawl_info_{self.dataset_id}.json')
