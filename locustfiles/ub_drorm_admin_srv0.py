import json
import random
import sys

from locust import FastHttpUser, task

import setting_user
import setting_header
from data_comp_code_drorm import comp_code
from data_pers_code_drorm import pers_code
from func import get_now_strftime


class DrormAdminUser_Srv0(FastHttpUser):
    class_name = __qualname__.split('_')[0]
    wait_time = setting_user.users.get(class_name).get('wait_time')
    host = setting_user.users.get(class_name).get('host')
    # fixed_count = setting_user.users.get(class_name).get('fixed_count')
    shw = setting_header.SettingHeadersWeb(class_name)
    headers = shw.headers
    serial = setting_user.users.get(class_name).get('serial')
    sbj_pers_code_list = pers_code
    sbj_comp_code_list = comp_code

    # Створення обтяження
    @task(2)
    def create_lmn(self):
        # Створення Заява про реєстрацію обтяження рухомого майна
        data_create_st = [
            {
                "entity": "ormUb_requestCard",
                "method": "performAction",
                "instance": "{\"reqSort\":1,\"reqType\":\"1\",\"stateRequest\":false,\"outDate\":\"2022-12-01T00:00:00.000Z\",\"limitation\":{\"lmSort\":\"1\",\"alPossible\":\"2\",\"contractSum\":\"1000\",\"currencyType\":\"грн\",\"execTerm\":\"\",\"actTerm\":\"\",\"lmType\":\"7\"},\"properties\":[{\"prAttr\":[],\"prCategory\":\"3\",\"prType\":11,\"prRegNum\":\"Y2\",\"mvSrNum\":\"АА1234АА\",\"prTypeExtension\":\"доп\"}],\"subjects\":[{\"sbjType\":\"1\",\"rlRlID\":\"10\",\"name\":\"Токарь Сергей Владимирович\",\"code\":\"1234567897\",\"document\":\"СН123456\",\"isSimpleAddress\":false},{\"sbjType\":\"2\",\"rlRlID\":\"11\",\"name\":\"ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ \\\"БК БУДІНВЕСТГРУП\\\"\",\"code\":\"33261467\",\"phone\":\"+380678881188\",\"isSimpleAddress\":true,\"simpleAddress\":\"Україна, 01024, місто Київ, ВУЛИЦЯ ДАРВІНА, будинок 5, квартира 10\",\"eedrEedrID\":317141},{\"sbjType\":\"1\",\"rlRlID\":\"15\",\"name\":\"Сорока Сергій Володимирович\",\"code\":\"3326146745\"}],\"causeDocuments\":[{\"cdTypeExtension\":\"документ-право\",\"serNum\":\"12\",\"pubDate\":\"2022-12-05T00:00:00.000Z\",\"publisher\":\"Приват Банк\"}],\"extract\":null,\"operationData\":{}}",
                "operation": "{\"acName\":\"rgreq\",\"ID\":null}",
                "privCode": "ADMIN_DRORM_REQUEST_OPERATIONS_REG"
            }
        ]
        response_create_st = self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya zayavi", headers=self.headers,
                                              json=data_create_st).json()[0]
        rn_num = response_create_st.get('rnNum')

        data_generate_print_doc = [
            {
                "entity": "ormUb_requestCard",
                "method": "generatePrintDocument",
                "rnNum": rn_num,
                "privCode": "ADMIN_DRORM_REQUEST_OPERATIONS_PRINT_DOC"
            }
        ]
        response_generate_print_doc = \
            self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya DF(print) zayavi", headers=self.headers,
                             json=data_generate_print_doc).json()[0]
        doc_id = response_generate_print_doc.get('docID')

        data_generate_pdf_doc = [
            {
                "entity": "ormUb_document",
                "fieldList": [
                    "generatedDocument",
                    "ID"
                ],
                "ID": doc_id,
                "method": "select"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya DF zayavi", headers=self.headers,
                         json=data_generate_pdf_doc)

        st_date_time = get_now_strftime("%Y-%m-%dT%H-2:%M:%S.000Z")
        data_sign_pdf_st_card = [
            {
                "entity": "ormUb_documentSignature",
                "method": "saveSignature",
                "sTime": st_date_time,
                "execParams": {
                    "docDocID": doc_id,
                    "signature": "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",
                    "timeStamp": st_date_time,
                    "serial": self.serial
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)pidpisannya zayavi", headers=self.headers,
                         json=data_sign_pdf_st_card)

        # Створення обтяження
        data_create_lmn = [
            {
                "entity": "ormUb_limitationCard",
                "method": "performAction",
                "instance": "{\"reqReqID\":" + str(rn_num) + ",\"regNum\":" + str(
                    rn_num) + ",\"lmType\":\"7\",\"lmSort\":\"1\",\"lmTypeExtension\":\"\",\"employeeId\":110167,\"execTerm\":null,\"actTerm\":\"2027-12-06T00:00:00.000Z\",\"contractSum\":\"1000\",\"currencyType\":\"грн\",\"alPossible\":\"2\",\"additional\":\"\",\"properties\":[{\"prType\":\"11\",\"prTypeExtension\":\"доп\",\"prCategory\":\"3\",\"prRegNum\":\"Y2\",\"mvRegNum\":null,\"otherRegNumNID\":null,\"reqReqID\":76306952,\"mvSrNum\":\"АА1234АА\",\"changeType\":\"1\",\"changeLmType\":null,\"additional\":null,\"prParentID\":null,\"otherRegNumHash\":null,\"otherRegNum\":null,\"mvSrNumHash\":\"aa1234aa\",\"mvRegNumHash\":null,\"isArchive\":null,\"prRegNumNID\":null,\"driRegDate\":null,\"driRegNum\":null,\"prAttr\":[],\"fieldsetType\":\"property\"}],\"subjects\":[{\"sbjType\":\"1\",\"subjectParentID\":null,\"atuAtuID\":null,\"cnCnID\":null,\"rlRlID\":\"10\",\"reqReqID\":76306952,\"nNID\":958587,\"foreignSubject\":null,\"birthMonth\":null,\"codeAbsence\":null,\"code\":\"1234567897\",\"changeType\":\"1\",\"changeLmType\":null,\"birthYear\":null,\"birthDay\":null,\"addressIndex\":null,\"additional\":null,\"birthDate\":null,\"birthPlace\":null,\"name\":\"Токарь Сергей Владимирович\",\"simpleAddress\":null,\"addressDetails\":null,\"document\":\"СН123456\",\"phone\":null,\"objObjID\":null,\"house\":null,\"building\":null,\"objectNum\":null,\"dcObjectNumType\":null,\"room\":null,\"dcHouseType\":null,\"dcRoomType\":null,\"dcCountry\":null,\"dcBuildingType\":null,\"eedrEedrID\":null,\"isAuthorizedPerson\":null,\"authorizedOrgName\":null,\"authorizedDocument\":null,\"codeAbsenceName\":\"\",\"fieldsetType\":\"subject\",\"isSimpleAddress\":false},{\"sbjType\":\"2\",\"subjectParentID\":null,\"atuAtuID\":null,\"cnCnID\":null,\"rlRlID\":\"11\",\"reqReqID\":76306952,\"nNID\":958886,\"foreignSubject\":null,\"birthMonth\":null,\"codeAbsence\":null,\"code\":\"33261467\",\"changeType\":\"1\",\"changeLmType\":null,\"birthYear\":null,\"birthDay\":null,\"addressIndex\":null,\"additional\":null,\"birthDate\":null,\"birthPlace\":null,\"name\":\"ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ \\\"БК БУДІНВЕСТГРУП\\\"\",\"simpleAddress\":\"Україна, 01024, місто Київ, ВУЛИЦЯ ДАРВІНА, будинок 5, квартира 10\",\"addressDetails\":null,\"document\":null,\"phone\":\"+380678881188\",\"objObjID\":null,\"house\":null,\"building\":null,\"objectNum\":null,\"dcObjectNumType\":null,\"room\":null,\"dcHouseType\":null,\"dcRoomType\":null,\"dcCountry\":null,\"dcBuildingType\":null,\"eedrEedrID\":317141,\"isAuthorizedPerson\":null,\"authorizedOrgName\":null,\"authorizedDocument\":null,\"codeAbsenceName\":\"\",\"fieldsetType\":\"subject\",\"isSimpleAddress\":true}],\"causeDocuments\":[{\"pubDate\":\"2022-12-05T00:00:00Z\",\"cdType\":null,\"serNum\":\"12\",\"additional\":null,\"publisher\":\"Приват Банк\",\"cdTypeExtension\":\"документ-право\",\"changeType\":\"1\",\"fieldsetType\":\"document\"}],\"operationData\":{}}",
                "operation": "{\"acName\":\"rglim\",\"ID\":null}",
                "privCode": "ADMIN_DRORM_LIMITATION_OPERATIONS_CREATE"
            }
        ]
        response_create_lmn = self.client.post("/ubql", name=self.class_name + " (DRORM)2-stvorennya obtyajennya", headers=self.headers,
                                               json=data_create_lmn).json()[0]
        op_op_id = response_create_lmn.get('opOpID')

        data_select_lmn = [
            {
                "entity": "ormUb_limitationCard",
                "method": "select",
                "privCode": "ADMIN_DRORM_LIMITATION_OPERATIONS_VIEW",
                "instance": {
                    "opOpID": op_op_id
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya (select) obtyajennya", headers=self.headers,
                         json=data_select_lmn)

        # Формування витягу
        data_generate_extract_vityag = [
            {
                "entity": "ormUb_limitationCard",
                "method": "generateExtract",
                "opOpID": op_op_id,
                "acName": "excreq",
                "privCode": "ADMIN_DRORM_LIMITATION_OPERATIONS_EXTRACT_REG"
            }
        ]
        response_generate_extract_vityag = self.client.post("/ubql", name=self.class_name + " (DRORM)2-stvorennya vityaga",
                                                            headers=self.headers,
                                                            json=data_generate_extract_vityag).json()[0]
        doc_id = response_generate_extract_vityag.get('docID')

        data_select_document_vityag = [
            {
                "entity": "ormUb_document",
                "fieldList": [
                    "generatedDocument",
                    "ID"
                ],
                "ID": doc_id,
                "method": "select"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya DF vityagu", headers=self.headers,
                         json=data_select_document_vityag)

        data_generated_document_vityag = {
            "entity": "ormUb_document",
            "attribute": "generatedDocument",
            "ID": doc_id,
            "store": "drormReports",
            "origName": '{doc_id}{pdf}'.format(doc_id=str(doc_id), pdf='.pdf'),
            "filename": 'ormUb_document{doc_id}generatedDocument'.format(doc_id=str(doc_id)),
            "_rc": 1
        }
        # self.client.get("/ubql", name=self.class_name + " (DRORM)2-vidkrittya DF vityaga", headers=self.headers,
        #                 params=data_generated_document_vityag)

    # Пошук по суб’єкту (РНОКПП) обтяження з формуванням витягу
    @task(4)
    def search_lmn_pers_code(self):
        # Створення Заява про надання інформації з Державного реєстру обтяжень рухомого майна
        sbj_сode = random.choice(self.sbj_pers_code_list)
        op_op_id = None

        data_create_st = [
            {
                "entity": "ormUb_requestCard",
                "method": "performAction",
                "instance": "{\"reqSort\":1,\"reqType\":\"5\",\"stateRequest\":false,\"outDate\":\"2022-12-06T00:00:00.000Z\",\"limitation\":null,\"properties\":[],\"subjects\":[{\"sbjType\":\"1\",\"rlRlID\":\"15\",\"name\":\"Сорока Сергій Володимирович\",\"code\":\"3326146745\"}],\"causeDocuments\":[],\"extract\":{\"infoType\":\"3\",\"isCheckSum\":\"0\",\"sbjType\":\"1\",\"sbjCode\":" + str(
                    sbj_сode) + "},\"operationData\":{}}",
                "operation": "{\"acName\":\"rgreq\",\"ID\":null}",
                "privCode": "ADMIN_DRORM_REQUEST_OPERATIONS_REG"
            }
        ]
        response_create_st = \
            self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya zayavi", headers=self.headers,
                             json=data_create_st).json()[0]
        rn_num = response_create_st.get('rnNum')

        data_generate_print_doc = [
            {
                "entity": "ormUb_requestCard",
                "method": "generatePrintDocument",
                "rnNum": rn_num,
                "privCode": "ADMIN_DRORM_REQUEST_OPERATIONS_PRINT_DOC"
            }
        ]
        response_generate_print_doc = \
            self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya (print) zayavi", headers=self.headers,
                             json=data_generate_print_doc).json()[0]
        doc_id = response_generate_print_doc.get('docID')

        data_generate_pdf_doc = [
            {
                "entity": "ormUb_document",
                "fieldList": [
                    "generatedDocument",
                    "ID"
                ],
                "ID": doc_id,
                "method": "select"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya DF zayavi", headers=self.headers,
                         json=data_generate_pdf_doc)

        st_date_time = get_now_strftime("%Y-%m-%dT%H-2:%M:%S.000Z")
        data_sign_pdf_st_card = [
            {
                "entity": "ormUb_documentSignature",
                "method": "saveSignature",
                "sTime": st_date_time,
                "execParams": {
                    "docDocID": doc_id,
                    "signature": "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",
                    "timeStamp": st_date_time,
                    "serial": self.serial
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)pidpisannya zayavi", headers=self.headers,
                         json=data_sign_pdf_st_card)

        data_search = [
            {
                "entity": "ormUb_search",
                "method": "searchExtract",
                "shortcutCode": "ADMIN_DRORM_EXTRACT_REGISTRY",
                "privPrefix": "ADMIN",
                "searchParams": "{\"reasonReqRnNum\":\"" + str(
                    rn_num) + "\",\"docType\":\"2\",\"sbjType\":\"1\",\"code\":\"" + str(
                    sbj_сode) + "\",\"isSimpleSearch\":true}"
            }
        ]

        response_search = self.client.post("/ubql", name=self.class_name + " (DRORM)poshuk obtyajennya po rnokpp ", headers=self.headers,
                                           json=data_search).json()[0]
        se_id = response_search.get('seID')
        if 'resultData' in response_search:
            result_data = json.loads(response_search.get('resultData'))
            op_op_id = random.choice(result_data).get('opOpID')

        data_generate_extract_registry = [
            {
                "entity": "ormUb_limitationCard",
                "method": "generateExtractRegistry",
                "seID": se_id,
                "docType": "2",
                "lmRnNum": op_op_id
            }
        ]
        response_generate_extract_registry = \
            self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya vitygu", headers=self.headers,
                             json=data_generate_extract_registry).json()[0]
        doc_id_vityag = response_generate_extract_registry.get('docID')

        data_select_document_vityag = [
            {
                "entity": "ormUb_document",
                "fieldList": [
                    "generatedDocument",
                    "ID"
                ],
                "ID": doc_id_vityag,
                "method": "select"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya DF vityagu", headers=self.headers,
                         json=data_select_document_vityag)

        data_generated_document_vityag = {
            "entity": "ormUb_document",
            "attribute": "generatedDocument",
            "ID": doc_id,
            "store": "drormReports",
            "origName": '{doc_id}{pdf}'.format(doc_id=str(doc_id), pdf='.pdf'),
            "filename": 'ormUb_document{doc_id}generatedDocument'.format(doc_id=str(doc_id)),
            "_rc": 1
        }
        # self.client.get("/ubql", name=self.class_name + " (DRORM)2-vidkrittya DF vityaga", headers=self.headers,
        #                 params=data_generated_document_vityag)

    # Пошук по суб’єкту (ЄДРПОУ) обтяження з формуванням витягу
    @task(4)
    def search_lmn_comp_code(self):
        # Створення Заява про надання інформації з Державного реєстру обтяжень рухомого майна
        sbj_сode = random.choice(self.sbj_comp_code_list)
        op_op_id = None

        data_create_st = [
            {
                "entity": "ormUb_requestCard",
                "method": "performAction",
                "instance": "{\"reqSort\":1,\"reqType\":\"5\",\"stateRequest\":false,\"outDate\":\"2022-12-06T00:00:00.000Z\",\"limitation\":null,\"properties\":[],\"subjects\":[{\"sbjType\":\"1\",\"rlRlID\":\"15\",\"name\":\"Сорока Сергій Володимирович\",\"code\":\"3326146745\"}],\"causeDocuments\":[],\"extract\":{\"infoType\":\"3\",\"isCheckSum\":\"0\",\"sbjType\":\"2\",\"sbjCode\":" + str(
                    sbj_сode) + "},\"operationData\":{}}",
                "operation": "{\"acName\":\"rgreq\",\"ID\":null}",
                "privCode": "ADMIN_DRORM_REQUEST_OPERATIONS_REG"
            }
        ]
        response_create_st = \
            self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya zayavi", headers=self.headers,
                             json=data_create_st).json()[0]
        rn_num = response_create_st.get('rnNum')

        data_generate_print_doc = [
            {
                "entity": "ormUb_requestCard",
                "method": "generatePrintDocument",
                "rnNum": rn_num,
                "privCode": "ADMIN_DRORM_REQUEST_OPERATIONS_PRINT_DOC"
            }
        ]
        response_generate_print_doc = \
            self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya (print) zayavi", headers=self.headers,
                             json=data_generate_print_doc).json()[0]
        doc_id = response_generate_print_doc.get('docID')

        data_generate_pdf_doc = [
            {
                "entity": "ormUb_document",
                "fieldList": [
                    "generatedDocument",
                    "ID"
                ],
                "ID": doc_id,
                "method": "select"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya DF zayavi", headers=self.headers,
                         json=data_generate_pdf_doc)

        st_date_time = get_now_strftime("%Y-%m-%dT%H-2:%M:%S.000Z")
        data_sign_pdf_st_card = [
            {
                "entity": "ormUb_documentSignature",
                "method": "saveSignature",
                "sTime": st_date_time,
                "execParams": {
                    "docDocID": doc_id,
                    "signature": "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",
                    "timeStamp": st_date_time,
                    "serial": self.serial
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)pidpisannya zayavi", headers=self.headers,
                         json=data_sign_pdf_st_card)

        data_search = [
            {
                "entity": "ormUb_search",
                "method": "searchExtract",
                "shortcutCode": "ADMIN_DRORM_EXTRACT_REGISTRY",
                "privPrefix": "ADMIN",
                "searchParams": "{\"reasonReqRnNum\":\"" + str(
                    rn_num) + "\",\"docType\":\"2\",\"sbjType\":\"2\",\"code\":\"" + str(
                    sbj_сode) + "\",\"isSimpleSearch\":true}"
            }
        ]

        response_search = self.client.post("/ubql", name=self.class_name + " (DRORM)poshuk obtyajennya po edrpou", headers=self.headers,
                                           json=data_search).json()[0]
        se_id = response_search.get('seID')
        if 'resultData' in response_search:
            result_data = json.loads(response_search.get('resultData'))
            op_op_id = random.choice(result_data).get('opOpID')

        data_generate_extract_registry = [
            {
                "entity": "ormUb_limitationCard",
                "method": "generateExtractRegistry",
                "seID": se_id,
                "docType": "2",
                "lmRnNum": op_op_id
            }
        ]
        response_generate_extract_registry = \
            self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya vitygu", headers=self.headers,
                             json=data_generate_extract_registry).json()[0]
        doc_id_vityag = response_generate_extract_registry.get('docID')

        data_select_document_vityag = [
            {
                "entity": "ormUb_document",
                "fieldList": [
                    "generatedDocument",
                    "ID"
                ],
                "ID": doc_id_vityag,
                "method": "select"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)stvorennya DF vityagu", headers=self.headers,
                         json=data_select_document_vityag)

        data_generated_document_vityag = {
            "entity": "ormUb_document",
            "attribute": "generatedDocument",
            "ID": doc_id,
            "store": "drormReports",
            "origName": '{doc_id}{pdf}'.format(doc_id=str(doc_id), pdf='.pdf'),
            "filename": 'ormUb_document{doc_id}generatedDocument'.format(doc_id=str(doc_id)),
            "_rc": 1
        }
        # self.client.get("/ubql", name=self.class_name + " (DRORM)2-vidkrittya DF vityaga", headers=self.headers,
        #                 params=data_generated_document_vityag)

    # Пошук заяв
    @task(15)
    def search_st(self):
        data = [
            {
                "entity": "ormUb_search",
                "method": "searchRequest",
                "shortcutCode": "ADMIN_DRORM_REQUEST_SEARCH",
                "privPrefix": "ADMIN",
                "searchParams": "{\"regStartDate\":\"2021-11-01T00:00:00.000Z\",\"regFinishDate\":\"2021-11-15T00:00:00.000Z\",\"isSimpleSearch\":true}"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)poshuk zayav", headers=self.headers, json=data)

    # Пошук обтяження
    @task(30)
    def search_lmn(self):
        sbj_comp_сode = random.choice(self.sbj_comp_code_list)
        sbj_pers_сode = random.choice(self.sbj_pers_code_list)
        sbj_code = random.choice([sbj_comp_сode, sbj_pers_сode])
        data = [
            {
                "entity": "ormUb_search",
                "method": "searchLimitation",
                "shortcutCode": "ADMIN_DRORM_LIMITATION_ADVSEARCH",
                "privPrefix": "ADMIN",
                "searchParams": "{\"property\":{\"prType\":[]},\"subject\":{\"rlRlID\":\"\\\"10\\\"\",\"code\":\"" + str(
                    sbj_code) + "\"},\"isSimpleSearch\":false}"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)poshuk obtyajen", headers=self.headers, json=data)

    # Пошук раніше сформованих документів
    @task(10)
    def search_generated_documents(self):
        data = [
            {
                "entity": "ormUb_search",
                "method": "searchDocument",
                "shortcutCode": "ADMIN_DRORM_REP_RSD",
                "privPrefix": "ADMIN",
                "searchParams": "{\"regStartDate\":\"2021-11-01T00:00:00.000Z\",\"regFinishDate\":\"2021-11-01T00:00:00.000Z\",\"docType\":\"\\\"2\\\"\",\"atuAtuID\":26,\"isSimpleSearch\":true}"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)poshuk ranishe sformovani dokumenti", headers=self.headers, json=data)

    @task(4)
    def summary_report_reg_action(self):
        reg_num_date = get_now_strftime('YYYY-MM-DDTHH:MM:SS.116Z')
        data = [
            {
                "entity": "ormUb_summaryReport",
                "method": "generate",
                "searchParams": {
                    "dcSdType": "4",
                    "regionAtuId": 10,
                    "organizationCategoryId": 910,
                    "organizationId": 82969,
                    "employeeId": 179072,
                    "code": "",
                    "acGroup": "\"1\",\"2\",\"3\"",
                    "startDate": "2021-11-01T00:00:00.000Z",
                    "endDate": "2021-12-01T00:00:00.000Z",
                    "outputFormat": "xlsx",
                    "regNumDate": reg_num_date
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRORM)formuvannya zvitu po registratoru", headers=self.headers, json=data)
