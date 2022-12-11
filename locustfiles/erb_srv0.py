import random
import sys

from locust import FastHttpUser, task

import setting_header
import setting_user


class ErbUser_Srv0(FastHttpUser):
    class_name = __qualname__.split('_')[0]
    wait_time = setting_user.users.get(class_name).get('wait_time')
    host = setting_user.users.get(class_name).get('host')
    # fixed_count = setting_user.users.get(class_name).get('fixed_count')
    shw = setting_header.SettingHeadersWeb(class_name)
    headers = shw.headers

    # Пошук по єдрпоу
    @task
    def search_comp_code(self):
        edrpou_list = ['05747991', '05393122', '14307423', '00306710']
        edrpou = random.choice(edrpou_list)
        data = {
            "searchType": "2",
            "paging": "1",
            "filter": {
                "FirmName": "",
                "FirmEdrpou": edrpou,
                "categoryCode": ""
            },
            "reCaptchaToken": "03AEkXODDpRKfMFGcQ17iBSxrNiw1znSuaO5H7U_teDvV1XK0iMozuq7Sy6YM25EOb27e5MFfaTiHQOiTJ26-nLYdpGJBzWn24Dfn9mmrZO8AgE7eew2sJyTq4JvR0MXgSkp2ii8tGrKwrIWpgwLraSY37ddiq8GI4dsq9AppdWBiG3bqzYt7iqBOyLIA-35S3gSc2aEthsGPFGbQAsypy0IV3RavW4d-UEOMT7ZY96Nz75QM_czH31EoaHDTcNJk6NS8P41Ur2F8YazxDcPzXdKzK1ew0Dc9iuopSY7huiBPyVMPUqGnzNPBdLlSZCk4eDKTmxzbB544izzCbo21Ch9r5-qx1ZY1_NitG1-ntBBOXchvy7Pf3qrPl0PJtc4-Mx6s-i00uQlG7uWk0Y6Vl6-mvEkNq0fD7dS5fGX6dhBZnyiMeE31-zQOpDHzRL3VJEXX4VZY03MZcoeV2So1EonghqfL7e_VW0itIMUfpyB_FqPxjkfnqjcYI8wDG7kszPGyZJFLfSq47jFoTkHutnpJrFNxZRS_p1g"
        }
        self.client.post('/listDebtorsEndpoint', name="(ERB)poshuk po Edrpou", headers=self.headers, json=data)

    # Пошук по ПІБ
    @task
    def search_pers_name(self):
        name_list = ['Малишева Надія Олександрівна', 'Тест Арнольд Степанович', 'Теляпова Неоніла Олександрівна']
        name = random.choice(name_list)
        t_name = tuple(map(str, name.split(' ')))

        data = {
            "searchType": "1",
            "paging": "1",
            "filter": {
                "LastName": t_name[0],
                "FirstName": t_name[1],
                "MiddleName": t_name[2],
                "BirthDate": None,
                "IdentCode": "",
                "categoryCode": ""
            },
            "reCaptchaToken": "03AEkXODDpRKfMFGcQ17iBSxrNiw1znSuaO5H7U_teDvV1XK0iMozuq7Sy6YM25EOb27e5MFfaTiHQOiTJ26-nLYdpGJBzWn24Dfn9mmrZO8AgE7eew2sJyTq4JvR0MXgSkp2ii8tGrKwrIWpgwLraSY37ddiq8GI4dsq9AppdWBiG3bqzYt7iqBOyLIA-35S3gSc2aEthsGPFGbQAsypy0IV3RavW4d-UEOMT7ZY96Nz75QM_czH31EoaHDTcNJk6NS8P41Ur2F8YazxDcPzXdKzK1ew0Dc9iuopSY7huiBPyVMPUqGnzNPBdLlSZCk4eDKTmxzbB544izzCbo21Ch9r5-qx1ZY1_NitG1-ntBBOXchvy7Pf3qrPl0PJtc4-Mx6s-i00uQlG7uWk0Y6Vl6-mvEkNq0fD7dS5fGX6dhBZnyiMeE31-zQOpDHzRL3VJEXX4VZY03MZcoeV2So1EonghqfL7e_VW0itIMUfpyB_FqPxjkfnqjcYI8wDG7kszPGyZJFLfSq47jFoTkHutnpJrFNxZRS_p1g"
        }
        self.client.post('/listDebtorsEndpoint', name="(ERB)poshuk po Pib", headers=self.headers, json=data)
