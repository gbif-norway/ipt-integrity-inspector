import luigi
from tasks.fetch_and_write_dataset_ids import FetchAndWriteDatasetIDs
import pandas as pd
from tasks.check_dataset import CheckDataset

class IPTCheck(luigi.Task):
    ipt_url = luigi.Parameter()

    def requires(self):
        return FetchAndWriteDatasetIDs(ipt_url=self.ipt_url)

    def run(self):
        with self.input().open('r') as infile:
            dataset_ids = pd.read_csv(infile)
        for dataset_id in dataset_ids['Dataset ID']:
            yield CheckDataset(dataset_id=dataset_id)
