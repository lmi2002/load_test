from locust import task, FastHttpUser

import setting_user
import setting_header


class AsvpDilovodUser_Srv0(FastHttpUser):
    class_name = __qualname__
    class_name_user = __qualname__.split('_')[0]
    wait_time = setting_user.users.get(class_name_user).get('wait_time')
    host = setting_user.users.get(class_name_user).get('host')
    # fixed_count = setting_user.users.get(class_name_user).get('fixed_count')
    shw = setting_header.SettingHeadersWeb(class_name_user)
    headers = shw.headers

    # Формування журналів реєстрації загальної вхідної кореспонденції
    @task
    def register_general_incoming_correspondence(self):
        data_search = [
            {
                "entity": "vp_dfInDocument",
                "method": "select",
                "fieldList": [
                    "incomeNum",
                    "incomeDate",
                    "senderName",
                    "senderNum",
                    "senderDate",
                    "inDocTypeID.name",
                    "description",
                    "vpID.orderNum",
                    "vdID.registerDate",
                    "controlDate",
                    "empID",
                    "empStr",
                    "incomeYear",
                    "executionNotes",
                    "executorCreateDate",
                    "isEReceive"
                ],
                "whereList": {
                    "c1": {
                        "expression": "[atuID]",
                        "condition": "equal",
                        "value": 26
                    },
                    "c2": {
                        "expression": "[depID]",
                        "condition": "equal",
                        "value": 84812
                    },
                    "byExecFrom": {
                        "expression": "[incomeDate]",
                        "condition": "moreEqual",
                        "value": "2021-11-01T00:00:00.000Z"
                    },
                    "byExecTo": {
                        "expression": "[incomeDate]",
                        "condition": "less",
                        "value": "2021-12-02T00:00:00.000Z"
                    }
                },
                "orderList": {
                    "0": {
                        "expression": "[incomeNum]",
                        "order": "asc"
                    }
                }
            }
        ]

        self.client.post("/ubql", name=self.class_name + " (ASVP)formuvannya jurnalu vhid. korespond", headers=self.headers,
                         json=data_search)

    # Формування журналів реєстрації загальної вихідної кореспонденції
    @task
    def register_general_outcoming_correspondence(self):
        data_search = [
            {
                "entity": "vp_dfOutDocument",
                "method": "select",
                "fieldList": [
                    "ID",
                    "outNum",
                    "outDate",
                    "outDocTypeDef",
                    "description",
                    "vpID.orderNum",
                    "addressees",
                    "pages",
                    "isESent",
                    "isError",
                    "outYear"
                ],
                "whereList": {
                    "byTypeCode": {
                        "expression": "[vpDocTypeID.code]",
                        "condition": "notIn",
                        "value": [
                            "240001",
                            "240101"
                        ]
                    },
                    "byTypeCodeEmpty": {
                        "expression": "[vpDocTypeID.code]",
                        "condition": "isNull",
                        "value": [
                            "240001",
                            "240101"
                        ]
                    },
                    "c1": {
                        "expression": "[atuID]",
                        "condition": "equal",
                        "value": 26
                    },
                    "c2": {
                        "expression": "[depID]",
                        "condition": "equal",
                        "value": 84812
                    },
                    "byExecFrom": {
                        "expression": "[outDate]",
                        "condition": "moreEqual",
                        "value": "2021-11-01T00:00:00.000Z"
                    },
                    "byExecTo": {
                        "expression": "[outDate]",
                        "condition": "less",
                        "value": "2021-12-02T00:00:00.000Z"
                    }
                },
                "orderList": {
                    "0": {
                        "expression": "[outNum]",
                        "order": "asc"
                    }
                },
                "logicalPredicates": [
                    "([byTypeCode] or [byTypeCodeEmpty])"
                ]
            }
        ]

        self.client.post("/ubql", name=self.class_name + " (ASVP)formuvannya jurnalu vihid. korespond", headers=self.headers,
                         json=data_search)


