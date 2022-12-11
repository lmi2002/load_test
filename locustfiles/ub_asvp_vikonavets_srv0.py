import sys

from locust import task, FastHttpUser

import setting_user
import setting_header


class AsvpVikonavetsUser_Srv0(FastHttpUser):
    class_name = __qualname__.split('_')[0]
    wait_time = setting_user.users.get(class_name).get('wait_time')
    host = setting_user.users.get(class_name).get('host')
    # fixed_count = setting_user.users.get(class_name).get('fixed_count')
    shw = setting_header.SettingHeadersWeb(class_name)
    headers = shw.headers

    def on_start(self):
        # Запуск формування звіту про виконання рішень щодо стягнення періодичних платежів органами та особами,
        # які здійснюють примусове виконання судових рішень і рішень інших
        data = [
            {
                "entity": "vp_report",
                "method": "buildReport",
                "reportTypeID": 1,
                "reportNameID": 19,
                "atuID": 26,
                "depID": 84812,
                "periodID": None,
                "isFreePeriod": True,
                "dateFrom": "2021-01-01T00:00:00.000Z",
                "dateTo": "2021-12-31T00:00:00.000Z",
                "paramsRep": "{\"frm\":{\"isAllCategory\":false,\"category\":\"\",\"isAllPersonSubType\":false,\"personSubType\":\"\",\"isAllPublisherType\":false,\"publisherType\":\"\"}}",
                "repLevel": "OBJECT",
                "isPv": "WITHOUT",
                "reportCode": "08.01"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (ASVP)formuvannya zvitu vskonannya rishen", headers=self.headers, json=data)

    # Пошук ВД за період
    @task
    def search_vd_period(self):
        data = [
            {
                "entity": "vp_vd",
                "method": "selectSearch",
                "fieldList": [
                    "vpID",
                    "vpID.zvpID.orderNum",
                    "vpID.orderNum",
                    "num",
                    "incomeDate",
                    "lastIncomeNum",
                    "vpID.mi_wfStateWithError",
                    "mi_wfStateForGrid",
                    "name",
                    "pubDate",
                    "vpID.beginDate",
                    "sum",
                    "sumCurrencyID",
                    "periodicalPayments",
                    "prosecutorQuery",
                    "atuID",
                    "atuStr",
                    "depID",
                    "depErc",
                    "empID",
                    "empStr",
                    "debtorStr",
                    "creditorStr",
                    "parentVpVirtualID",
                    "advacePaid",
                    "advacePaidDate",
                    "advacePaidNum",
                    "advacePaidSum",
                    "advacePaidCurrencyID",
                    "vpID.isZvp",
                    "vpID.zvpID",
                    "ID"
                ],
                "searchParams": {
                    "vpID.isZvp": {
                        "value": False
                    },
                    "atuID": {
                        "value": 26
                    },
                    "isPv": {
                        "value": False
                    },
                    "depID": {
                        "value": 84812
                    },
                    "debtors.type": "debtorDefaultType",
                    "creditors.type": "creditorDefaultType",
                    "decisions.acceptDate": {
                        "from": "2022-11-30T22:00:00.000Z",
                        "to": "2022-12-30T22:00:00.000Z"
                    },
                    "decisions.typeID": {
                        "value": 201629080
                    }
                },
                "options": {
                    "limit": 100,
                    "start": 0
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (ASVP)poshuk po VD za period", headers=self.headers, json=data)

    # Пошук ВП по боржнику
    @task
    def search_vp_debtor(self):
        data = [
            {
                "entity": "vp_vpCard",
                "method": "selectSearch",
                "fieldList": [
                    "vdID",
                    "zvpID.orderNum",
                    "orderNum",
                    "vdID.num",
                    "vdID.incomeDate",
                    "vdID.lastIncomeNum",
                    "mi_wfStateWithError",
                    "vdID.mi_wfStateForGrid",
                    "vdID.name",
                    "vdID.pubDate",
                    "beginDate",
                    "vdID.sum",
                    "vdID.sumCurrencyID",
                    "vdID.periodicalPayments",
                    "vdID.prosecutorQuery",
                    "atuID",
                    "atuStr",
                    "depID",
                    "depErc",
                    "empID",
                    "empStr",
                    "debtorStr",
                    "creditorStr",
                    "vdID.parentVpVirtualID",
                    "vdID.advacePaid",
                    "vdID.advacePaidDate",
                    "vdID.advacePaidNum",
                    "vdID.advacePaidSum",
                    "vdID.advacePaidCurrencyID",
                    "isZvp",
                    "zvpID",
                    "ID"
                ],
                "searchParams": {
                    "vpID.isZvp": {
                        "value": False
                    },
                    "atuID": {
                        "value": 26
                    },
                    "isPv": {
                        "value": False
                    },
                    "depID": {
                        "value": 84812
                    },
                    "vpID.mi_wfStateVp": {
                        "values": [
                            "OPEN",
                            "ENFORCE"
                        ]
                    },
                    "debtors.type": "debtorPhysical",
                    "debtors.name": {
                        "value": "Анохін Віталій Вікторович"
                    },
                    "creditors.type": "creditorDefaultType"
                },
                "options": {
                    "limit": 100,
                    "start": 0
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (ASVP)poshuk VP za PIB", headers=self.headers, json=data)

    # Пошук ВП по аліменти
    @task
    def search_vp_alimentyi(self):
        data = [
            {
                "entity": "vp_vpCard",
                "method": "selectSearch",
                "fieldList": [
                    "vdID",
                    "zvpID.orderNum",
                    "orderNum",
                    "vdID.num",
                    "vdID.incomeDate",
                    "vdID.lastIncomeNum",
                    "mi_wfStateWithError",
                    "vdID.mi_wfStateForGrid",
                    "vdID.name",
                    "vdID.pubDate",
                    "beginDate",
                    "vdID.sum",
                    "vdID.sumCurrencyID",
                    "vdID.periodicalPayments",
                    "vdID.prosecutorQuery",
                    "atuID",
                    "atuStr",
                    "depID",
                    "depErc",
                    "empID",
                    "empStr",
                    "debtorStr",
                    "creditorStr",
                    "vdID.parentVpVirtualID",
                    "vdID.advacePaid",
                    "vdID.advacePaidDate",
                    "vdID.advacePaidNum",
                    "vdID.advacePaidSum",
                    "vdID.advacePaidCurrencyID",
                    "isZvp",
                    "zvpID",
                    "ID"
                ],
                "searchParams": {
                    "vpID.isZvp": {
                        "value": False
                    },
                    "atuID": {
                        "value": 26
                    },
                    "isPv": {
                        "value": False
                    },
                    "depID": {
                        "value": 84812
                    },
                    "vdID.categoryID": {
                        "value": 3
                    },
                    "vpID.mi_wfStateVp": {
                        "value": "OPEN"
                    },
                    "debtors.type": "debtorDefaultType",
                    "creditors.type": "creditorDefaultType"
                },
                "options": {
                    "limit": 100,
                    "start": 0
                }
            }
        ]

        self.client.post("/ubql", name=self.class_name + " (ASVP)poshuk VP alimenti", headers=self.headers, json=data)
