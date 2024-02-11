#%%
from tasks.ipt_check import IPTCheck
import os
import json
import luigi
#%%
if __name__ == '__main__':
    settings_txt = os.getenv('SETTINGS')
    print(settings_txt)
    settings = json.loads(settings_txt)
    tasks = [IPTCheck(ipt_url=x) for x in settings['ipt_servers']]
    luigi.build(tasks, local_scheduler=True)

