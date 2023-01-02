import random
import sys

from locust import FastHttpUser, task

import setting_user
import setting_header
from data_pers_name_drorm import pers_name


class DrormBankUser_Srv0(FastHttpUser):
    class_name = __qualname__
    class_name_user = __qualname__.split('_')[0]
    wait_time = setting_user.users.get(class_name_user).get('wait_time')
    host = setting_user.users.get(class_name_user).get('host')
    # fixed_count = setting_user.users.get(class_name_user).get('fixed_count')
    shw = setting_header.SettingHeadersWeb(class_name_user)
    headers = shw.headers
    sbj_pers_name_list = pers_name

    # Попередній пошук обтяжень
    @task
    def drorm_preliminary_search(self):
        sbj_name = random.choice(pers_name)
        data = [
            {
                "entity": "ormUb_search",
                "method": "searchPrevLimitation",
                "shortcutCode": "INFO_DRORM_PREV_LIMITATION",
                "privPrefix": "INFO",
                "searchParams": "{\"sbjType\":\"1\",\"nameUkr\":\"" + sbj_name + "\",\"isSimpleSearch\":true}"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)poperedniy poshuk obtyajen", headers=self.headers, json=data)
