import luigi
import requests
import csv
from xml.etree import ElementTree as ET

class FetchAndWriteDatasetIDs(luigi.Task):
    ipt_url = luigi.Parameter()

    def run(self):
        # Fetch RSS feed
        response = requests.get(f"{self.ipt_url}/rss.do")
        if response.status_code != 200:
            raise Exception("Failed to fetch RSS feed")

        # Parse RSS feed
        root = ET.fromstring(response.content)
        dataset_ids = []

        for item in root.findall('.//item/guid'):
            guid_text = item.text
            # Check if GUID is in the expected GBIF format (UUID/vX.X)
            if "http" not in guid_text:  # Assuming non-GBIF datasets have 'http' in their GUID
                dataset_id = guid_text.split('/')[0]
                dataset_ids.append(dataset_id)

        # Write dataset IDs to CSV
        with self.output().open('w') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['Dataset ID'])
            for dataset_id in dataset_ids:
                csv_writer.writerow([dataset_id])

    def output(self):
        safe_url = self.ipt_url.replace('https://','').replace('.','_').replace('/','_')
        return luigi.LocalTarget(f'/tmp/{safe_url}_dataset_ids.csv')

if __name__ == '__main__':
    luigi.build([FetchAndWriteDatasetIDs(ipt_url='https://ipt.gbif.no')])
