import json
import sys
import random

from locust import FastHttpUser, task

import setting_header
import setting_user
from data_pers_code_drrp import pers_code


class ObuApiUser_Srv0(FastHttpUser):
    class_name = __qualname__.split('_')[0]
    wait_time = setting_user.users.get(class_name).get('wait_time')
    host = setting_user.users.get(class_name).get('host')
    # fixed_count = setting_user.users.get(class_name).get('fixed_count')
    sha = setting_header.SettingHeadersApi(class_name)
    headers = sha.headers
    sbj_pers_code_list = pers_code

    @task
    def pkg_info_obu_sbj_code(self):
        sbj_сode = random.choice(self.sbj_pers_code_list)
        data_get_id = [
            {
                "entity": "pkg_infoRrp",
                "method": "getId"
            }
        ]
        response_get_id = \
            self.client.post("/ubql", name="(DRRP-API)11-Infodovidka z OBU getId", headers=self.headers,
                             json=data_get_id).json()[0]
        id = response_get_id.get('resultData')

        data_upload_package = [
            {
                "entity": "pkg_infoRrp",
                "method": "uploadPackage",
                "id": id,
                "packageContent": "{\"time\":\"2019-01-08T23:53:38+02:00\",\"version\":\"2.0\",\"userInfo\":{\"userName\":\"никитина1849\",\"userType\":\"1\",\"userCode\":\"1234567890\",\"userPassport\":\"АА458978\"},\"searchParams\":{\"reason\":\"Надання інформаційной довідки через реестраціїний портал\",\"searchType\":\"2\",\"subjectSearchInfo\":{\"sbjType\":\"1\",\"sbjCode\":\"" + str(sbj_сode) + "\"}}}"
            }
        ]
        response_upload_package = \
            self.client.post("/ubql", name="(DRRP-API)11-Infodovidka z OBU uploadPackage", headers=self.headers,
                             json=data_upload_package).json()[0]
        result_data = json.loads(response_upload_package.get('resultData'))
        report_result_id = result_data.get('reportResultID')
        group_result_id = result_data.get('groupResult')[0].get('ID')

        data_generate_pdf = [
            {
                "entity": "pkg_infoRrp",
                "method": "generatePdf",
                "id": id,
                "reportResultID": report_result_id,
                "groupID": group_result_id
            }
        ]

        self.client.post("/ubql", name="(DRRP-API)11-Infodovidka z OBU generatePdf", headers=self.headers,
                         json=data_generate_pdf)
        data_get_result = [
            {
                "entity": "pkg_infoRrp",
                "method": "getResult",
                "id": id
            }
        ]
        self.client.post("/ubql", name="(DRRP-API)11-Infodovidka z OBU getResult", headers=self.headers,
                         json=data_get_result)
