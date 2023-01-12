import json
import os
import random

from locust import task, FastHttpUser

import setting_user
import setting_header
from data_atu_atu import atu_atu_locality, atu_atu_object, atu_atu_street, atu_region
from data_onm_drrp import onm_num
from data_erk_ import erc_employee, erc_object_atu, erc_objects_names_atu
from data_property_drrp import pr_num
from data_rpvn_drrp import rpvn_num
from data_rrp_core_dict_enum import rrp_core_dict_enum
from func import get_text_from_file, get_now_strftime, get_date_strftime
from data_comp_code import comp_code


class DrrpNotarUser_Srv0(FastHttpUser):
    class_name = __qualname__
    class_name_user = __qualname__.split('_')[0]
    wait_time = setting_user.users.get(class_name_user).get('wait_time')
    # fixed_count = setting_user.users.get(class_name_user).get('fixed_count')
    host = 'https://ub-srv-51.test.nais.gov.ua'
    shw = setting_header.SettingHeadersWeb(class_name_user)
    headers = shw.headers
    headers['authorization'] = 'UB e646b2ef63b742a189c03944'
    serial = setting_user.users.get(class_name_user).get('serial')
    onm_num_list = onm_num
    rpvn_num_list = rpvn_num
    pr_num_list = pr_num
    sbj_comp_code_list = comp_code

    # Обмін с ДЗК
    @task(4)
    def exchange_dzk(self):
        data_dzk = [
            {
                "entity": "rrpUb_request",
                "method": "getDZKInfo",
                "cadNum": "8000000000:75:114:0010"
            }
        ]

        self.client.post("/ubql", name=self.class_name + " (DRRP)1-obmіn dzk", headers=self.headers, json=data_dzk)

    # Обмін с ДСП
    @task(4)
    def exchange_dps_rnokpp(self):
        data_dps_rnokpp = [
            {
                "entity": "exch_dps",
                "method": "getSubjects",
                "sbjCode": "2564489755",
                "surname": "КІЛЮХ",
                "firstName": "РАНІЛЬ",
                "patronymic": "ЄСЕЙОВИЧ",
                "dcEntityType": "1",
                "sign": "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"
            }
        ]

        self.client.post("/ubql", name=self.class_name + " (DRRP)1-obmіn dps rnokpp", headers=self.headers,
                         json=data_dps_rnokpp)

    # Обмін с ЄДЕССБ
    @task(4)
    def exchange_edesssb(self):
        data_edesssb = [
            {
                "entity": "rrpDoc_causeDocument",
                "method": "getDabiDocument",
                "rnNum": "TI01:1528-6997-1067-0276",
                "dcCdType": "217"
            }
        ]

        response_get_edesssb = self.client.post(
            "/ubql", name=self.class_name + " (DRRP)1-obmin edessb (tex nomer edessb)", headers=self.headers,
            json=data_edesssb)

        document = response_get_edesssb.json()[0].get('document')
        orig_name = json.loads(document).get('storeItemMetadata').get('origName')

        data_get_edesssb_pdf = {
            "entity": "rrpDoc_digitalDocumentPageFile",
            "attribute": "generatedDocument",
            "id": orig_name,
            "isDirty": "true",
        }

        # self.client.get("/getDocument", name=self.class_name + " vidkrittya DF doc edessb", headers=self.headers, params=data_get_edesssb_pdf,
        #                 debug_stream=sys.stderr)

    # Перевірка ОНМ
    @task(6)
    def get_reg_num_onm(self):
        onm_num = random.choice(self.onm_num_list)
        data_reg_num_onm = [
            {
                "entity": "rrpUb_requestCard",
                "method": "checkRequestEntity",
                "checkParams": {
                    "dcEntityClass": "2",
                    "rnNum": str(onm_num),
                    "dcReqType": "19",
                    "dcReqRegType": "1"
                }
            }
        ]

        self.client.post("/ubql", name=self.class_name + " (DRRP)1-perevirka reg nomera u zayavi", headers=self.headers,
                         json=data_reg_num_onm)

    # Перевірка ПВ
    @task(6)
    def get_num_property(self):
        pr_num = random.choice(self.pr_num_list)
        data_num_property = [
            {
                "entity": "rrpUb_requestCard",
                "method": "checkRequestEntity",
                "checkParams": {
                    "rnNum": str(pr_num),
                    "dcEntityClass": "6",
                    "dcReqType": "19",
                    "dcReqRegType": "1",
                    "dcPrKind": "1"
                }
            }
        ]

        self.client.post("/ubql", name=self.class_name + " (DRRP)1-perevirka nomera prava vlastnosti u zayavi",
                         headers=self.headers,
                         json=data_num_property)

    # Обмін с ДСА
    @task(6)
    def exchange_dsa(self):
        data_dsa = [
            {
                "entity": "rrpExch_rsrSearch",
                "method": "search",
                "sign": "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",
                "reqRnNum": 51230791,
                "reqRegDate": "2022-11-28T10:44:39Z",
                "searchParams": {
                    "docDate": "2020-09-24T00:00:00.000Z",
                    "caseNum": "910/16312/19",
                    "docTypeID": 5,
                    "courtID": "5011"
                }
            }
        ]
        self.client.post("ubql=", name=self.class_name + " (DRRP)1-obmin dsa", headers=self.headers, json=data_dsa)

    # Перевірка РПВН
    @task(6)
    def get_rpvn(self):
        rpvn_num = random.choice(self.rpvn_num_list)
        data_rpvn = [
            {
                "entity": "rrpSec_propertyCard",
                "method": "selectOldRegistriesData",
                "queryParameters": {
                    "oldRegNum": str(rpvn_num)
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)1-perevirka rpvn u pravi vlastnosti",
                         headers=self.headers,
                         json=data_rpvn)

    # Реєстраційні дії користувача
    @task(1)
    def reg_action(self):
        # Реєстрація заяви ПВ
        data_create_st_card = json.loads(
            get_text_from_file(os.path.abspath('./data/data_create_st_card.txt')))
        response_create_st_card = self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya zayavi",
                                                   headers=self.headers,
                                                   json=data_create_st_card)
        rn_num = response_create_st_card.json()[0].get('rnNum')
        id = response_create_st_card.json()[0].get('ID')

        data_generate_pdf_st_card = [
            {
                "entity": "rrpUb_requestSearch",
                "method": "generatePdf",
                "requestInfoRecord": "{\"ID\":" + str(id) + ",\"reqReqID\":null,\"rnNum\":" + str(
                    rn_num) + ",\"dcReqState\":\"6\",\"holderObjID\":22061,\"holderObjnID\":4367,\"reqTypeExtension\":null,\"signDate\":null,\"outNum\":\"1\",\"senderEmpID\":null,\"formatVersion\":2,\"receiverObjID\":null,\"receiverObjnID\":null,\"regDate\":\"2022-11-23T23:22:37Z\",\"reqCode\":null,\"additional\":\"API\",\"senderObjID\":null,\"senderObjnID\":null,\"createDate\":null,\"receiverAtuID\":null,\"dcReqType\":\"19\",\"dcReqRegType\":\"1\",\"regNum\":\"51230684\",\"isActual\":\"1\",\"senderAtuID\":null,\"dcReqSort\":\"2\",\"holderAtuID\":10,\"dcDocReceiveType\":null,\"outDate\":\"2022-11-22T00:00:00Z\",\"rrbRrbID\":58601996,\"sendDate\":null,\"transferDate\":null,\"mi_wfState\":\"6\",\"dcDocGiveType\":\"1\",\"isReducedTerm\":null,\"dcExtReceiveType\":\"2\",\"extEmail\":null,\"dcTermReview\":\"7200\",\"dcApproveState\":4,\"termReviewDate\":\"2022-11-28T23:22:00Z\",\"body\":{\"ID\":58601996,\"isPrLimited\":null,\"rbDescription\":null,\"enum\":null,\"enumIrp\":null,\"enumPr\":null,\"dcDocTypeInfo\":null,\"entityLastOpID\":null,\"dcPrCommonKind\":null,\"lmTypeExtension\":null,\"decEnum\":null,\"enumReq\":null,\"dcReqDocType\":null,\"descriptionLmObject\":null,\"dcPrType\":null,\"additional\":null,\"changesDescription\":null,\"dcRecType\":null,\"rnNumBrealty\":null,\"irpPrTypeExtension\":null,\"isUndefined\":null,\"dcCourtDecision\":null,\"isExtractNeed\":null,\"dcCancelKind\":null,\"enumRealty\":null,\"dcDocReqType\":null,\"rnNumRealty\":null,\"dcIrpSortReq\":null,\"dcLmType\":null,\"dcEnumType\":null,\"series\":null,\"num\":null,\"enumBrealty\":null,\"dcEntityChangeTypeBit\":\"x000001\",\"isOwner\":null,\"dcReqTypeSubject\":null,\"startDate\":null,\"finishDate\":null,\"cadNum\":null,\"dcPrKind\":\"1\",\"dcEasementType\":null,\"easementTypeExtension\":null,\"isContractEmphyteutist\":null,\"dcSearchType\":null,\"dcErrorType\":null,\"dcRecTypeLnkTo\":null,\"entityChangeTypeBit\":\"набуття\",\"docTypeInfo\":\"<не вказано>\",\"prKind\":\"право власності\"},\"subjects\":[{\"ID\":104966297,\"rsbjRsbjID\":null,\"reqReqID\":60885663,\"sbjAdPostalID\":null,\"sbjAdLocationID\":null,\"cdCdID\":null,\"rnRnID\":13134294,\"sbjName\":\"КІЛЮХ РАНІЛЬ ЄСЕЙОВИЧ\",\"sbjCode\":\"2564489755\",\"dcCodeAbsenceBit\":null,\"dcSbjType\":\"1\",\"isState\":null,\"dcSbjRlNameBit\":\"x11\",\"dcChangeType\":\"2\",\"additional\":null,\"rnNum\":104966297,\"rSubjectRsbjID\":null,\"dcEntityClass\":\"1\",\"reqRnNum\":51230684,\"dcSbjSort\":\"1\",\"dcCountry\":\"225\",\"phone\":null,\"dcSbjAddType\":null,\"sbjPos\":null,\"idEddr\":null,\"isValidated\":1,\"isDmsValidated\":0,\"isNotResident\":null,\"reasonAbsentValidate\":null,\"surname\":\"КІЛЮХ\",\"firstName\":\"РАНІЛЬ\",\"patronymic\":\"ЄСЕЙОВИЧ\",\"taxNumber\":null,\"phoneNumber\":null,\"email\":null,\"isLocalGovernment\":null,\"sbjRlName\":\"Заявник; Суб’єкт права\",\"sbjType\":\"фізична особа\",\"country\":\"Україна\"}],\"realties\":[{\"ID\":54020835,\"rreRreID\":null,\"reqReqID\":60885663,\"reSubTypeExtension\":null,\"sbjCode\":null,\"sbjName\":null,\"enum\":null,\"dcChangeType\":\"2\",\"dcReType\":\"1\",\"dcReTypeOnm\":\"1\",\"description\":null,\"reqRnNum\":51230684,\"isFewAreaLoc\":null,\"sbjRegDate\":null,\"reTypeExtension\":null,\"dcReSubType\":null,\"renRenID\":null,\"rnNum\":54020835,\"dcIrpSpread\":null,\"enumSPart\":null,\"enumSubPart\":null,\"enumEmph\":null,\"objectIdentifier\":null,\"reExtension\":null,\"addresses\":[{\"ID\":39785395,\"rreRreID\":54020835,\"rrpRrpID\":null,\"atuAtuID\":null,\"house\":null,\"building\":null,\"objectNum\":null,\"rrpRnNum\":null,\"houseHash1\":null,\"houseHash2\":null,\"roomHash1\":null,\"additional\":null,\"dcObjectNumType\":null,\"room\":null,\"isNotFull\":null,\"dcReOwnerKind\":\"1\",\"simpleAddress\":null,\"isSimpleAddress\":\"0\",\"objectNumHash1\":null,\"objectNumHash2\":null,\"roomHash2\":null,\"dcHouseType\":null,\"dcRoomType\":null,\"groupNum\":1,\"buildingHash2\":null,\"dcBuildingType\":null,\"buildingHash1\":null,\"addressInfo\":\"\"}],\"cadNums\":[{\"ID\":36556042,\"rrpRrpID\":null,\"rreRreID\":54020835,\"enum\":\"8000000000:85:289:0006\",\"rrpRnNum\":null,\"cadNumHash\":\"8000000000852890006\"}],\"reType\":\"земельна ділянка\",\"reTypeOnm\":\"земельна ділянка\"}],\"paymentDocuments\":[{\"ID\":102820242,\"rpdRpdID\":null,\"reqReqID\":60885663,\"enum\":\"22\",\"pdType\":null,\"dcPayType\":\"5\",\"summ\":100,\"dcChangeType\":\"2\",\"dcPdReasonType\":null,\"rnNum\":102820242,\"additional\":null,\"reqRnNum\":51230684,\"orgName\":\"банк\",\"dcPdKind\":\"1\",\"rpdDate\":\"2022-11-23T00:00:00Z\",\"pdReasonTypeExtension\":null,\"reportResultID\":null,\"receiptNum\":null,\"payType\":\"Адміністративний збір за реєстраційні дії\"}],\"causeDocuments\":[{\"ID\":338459458,\"cdCdID\":null,\"dcCdSort\":\"1\",\"dcCdType\":\"108\",\"publisher\":\"Державний земельний кадастр\",\"enum\":\"55241333\",\"dcCdReasonType\":null,\"attrReqRnNum\":null,\"rceRnNum\":null,\"baseCdID\":null,\"ropRopID\":null,\"lmLmID\":null,\"mgMgID\":null,\"irpIrpID\":null,\"dcChangeType\":\"2\",\"bnRnNum\":null,\"baseRnNum\":null,\"prRnNum\":null,\"docTypeUser\":null,\"additional\":null,\"reqReqID\":60885663,\"rnNum\":338459458,\"lmRnNum\":null,\"dcCdKind\":\"12\",\"dcEntityClass\":\"1\",\"cdTypeExtension\":null,\"cdReasonTypeExtension\":null,\"rceRceID\":null,\"attrReqID\":null,\"reqRnNum\":51230684,\"irpRnNum\":null,\"bnBnID\":null,\"docDate\":\"2022-11-23T00:00:00Z\",\"expirationDate\":null,\"opOpID\":null,\"reReID\":null,\"mgRnNum\":null,\"breRnNum\":null,\"oedOedID\":null,\"reRnNum\":null,\"prPrID\":null,\"breBreID\":null,\"documentID\":355127189,\"cdType\":\"відомості з ДЗК\",\"pagesCount\":1,\"sortOrder\":355127189,\"uploadedPages\":1,\"countPages\":null,\"deliveryDate\":null,\"rercRercID\":null,\"pageFiles\":[{\"ID\":228952387,\"documentID\":355127189,\"pageNumber\":1,\"cdID\":338459458,\"empEmpID\":25213,\"dcCdType\":\"108\",\"addedDate\":\"2022-11-23T23:22:37Z\",\"signature\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"16419913.p7s\\\",\\\"origName\\\":\\\"16419913.p7s\\\",\\\"relPath\\\":\\\"202211/23\\\",\\\"ct\\\":\\\"application/pkcs7-signature\\\",\\\"size\\\":3782,\\\"md5\\\":\\\"6796e4a412fb99a266b0eb1212c12a1e\\\",\\\"revision\\\":1}\",\"generatedDocument\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"no-file-name.bin\\\",\\\"origName\\\":\\\"no-file-name.bin\\\",\\\"relPath\\\":\\\"202211/23\\\",\\\"ct\\\":\\\"application/octet-stream\\\",\\\"size\\\":54327,\\\"md5\\\":\\\"f2a2cd35936b5c29dcba9a24f7363d6b\\\",\\\"revision\\\":1}\"}],\"isDabiEcd\":true}],\"dzk\":[{\"ID\":18719019,\"areaUnit\":\"га\",\"dcAreaUnit\":null,\"techDoc\":\"Проект землеустрою щодо відведення земельних ділянок, 26.05.2008\",\"ownershipForm\":\"Комунальна власність\",\"cadNum\":\"8000000000:85:289:0006\",\"purpose\":\"Для розміщення та експлуатації основних, підсобних і допоміжних будівель та споруд підприємств переробної, машинобудівної та іншої промисловості\",\"regDate\":\"2008-05-30T00:00:00Z\",\"reqReqID\":60885663,\"state\":\"зареєстровано\",\"orgName\":\"Головне управління земельних ресурсів виконавчого органу Київради (Київської міської державної адміністрації)\",\"area\":\"1.4415\",\"purposeCode\":\"11.02\",\"cdCdID\":338459458,\"ddpfDdpfID\":228952387,\"address\":[{\"ID\":18565699,\"building\":\"40\",\"block\":null,\"rdzkRdzkID\":18719019,\"streetName\":\"вул. Фрунзе\",\"region\":\"м. Київ\",\"settlement\":null,\"streetType\":null,\"additionalInfoBlock\":null,\"district\":\"м. Київ\"}],\"subject\":[{\"ID\":22044813,\"sbjCode\":\"22883141\",\"name\":null,\"docReasonCompany\":null,\"docRightNumber\":null,\"rdzkRdzkID\":18719019,\"type\":\"юридична особа\",\"docRightType\":null,\"part\":\"1/1\",\"docRightDate\":null,\"passport\":null,\"docReasonNumber\":null,\"legalMode\":\"Право власності\",\"docReasonType\":null,\"servitudeMode\":null,\"irpDate\":null,\"irpTerm\":null,\"irpArea\":null,\"docRightCompany\":null,\"docReasonDate\":null}]}],\"holder\":{\"empEmpID\":25213,\"objObjID\":22061,\"objObjnID\":4367,\"atuAtuID\":10,\"objectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"objectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"atuName\":\"Київська обл.\",\"notaryDepName\":\"Фастівський районний нотаріальний округ\"},\"reqState\":\"зареєстровано\",\"lastOpID\":168554009,\"registrarEmpID\":25213,\"registrarEmployeeName\":\"Панікар Валентина Миколаївна\",\"registrarAtuID\":10,\"registrarAtuName\":\"Київська обл.\",\"registrarObjID\":22061,\"registrarObjectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"registrarObjnID\":4367,\"registrarObjectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"registrarInfo\":\"<b>Панікар Валентина Миколаївна</b>, Києво-Святошинська районна державна нотаріальна контора, Київська обл.\",\"registrarInfoExists\":true,\"reqType\":\"заява про державну реєстрацію прав\",\"reqSort\":\"паперова\",\"docGiveType\":\"особисто\",\"extReceiveType\":\"у паперовому вигляді\",\"holderEmpID\":25213,\"holderEmployeeName\":\"Панікар Валентина Миколаївна\",\"holderObjectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"holderObjectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"holderAtuName\":\"Київська обл.\",\"operations\":[{\"ID\":168554009,\"dcOpType\":\"1\",\"opDate\":\"2022-11-23T23:22:37Z\",\"empEmpID\":25213,\"objObjID\":22061,\"objObjnID\":4367,\"atuAtuID\":10,\"dcOpReasonType\":null,\"opReasonTypeExtension\":null,\"opReason\":null,\"additional\":null,\"registrarEmpID\":25213,\"registrarObjID\":22061,\"registrarObjnID\":4367,\"registrarAtuID\":10,\"dcEntityClass\":\"1\",\"isLastOp\":\"1\",\"dsRnNum\":null,\"toHID\":130781310,\"reasonDsRnNum\":null,\"cancelRopID\":null,\"objectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"registrarObjectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"objectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"registrarObjectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"opType\":\"Реєстрація заяви\",\"employeeName\":\"Панікар Валентина Миколаївна\",\"registrarEmployeeName\":\"Панікар Валентина Миколаївна\",\"atuName\":\"Київська обл.\",\"registrarAtuName\":\"Київська обл.\",\"entityClass\":\"заява\"}],\"decisionsAndDocs\":[],\"colorClass\":\"#ffd000\",\"isExistsPrintDoc\":0}",
                "repReportResultID": None,
                "isAllowAnnullate": False,
                "privPrefix": "NOTAR",
                "operation": "RequestPdf"
            }
        ]

        response_generate_pdf_st_card = self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya DF zayavi",
                                                         headers=self.headers,
                                                         json=data_generate_pdf_st_card)
        report_result_id_generate_st_pdf = response_generate_pdf_st_card.json()[0].get('reportResultID')

        data_get_doc_st_pdf = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id_generate_st_pdf,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id_generate_st_pdf),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id_generate_st_pdf)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)vidkrittya DF zayavi", headers=self.headers,
        #                 params=data_get_doc_st_pdf)

        data_select_st = [
            {
                "entity": "rrpUb_requestCard",
                "method": "select",
                "instance": {
                    "regNum": rn_num
                },
                "queryOptions": {
                    "causeDocuments": {
                        "orderList": {
                            "byCdSort": {
                                "expression": "[dcCdSort]",
                                "order": "asc"
                            }
                        }
                    }
                },
                "privCode": "NOTAR_REQUEST_OPERATIONS_VIEW"
            }
        ]

        response_select_st = self.client.post("/ubql", name=self.class_name + " (DRRP)2-vidkrittya formu zayavi",
                                              headers=self.headers,
                                              json=data_select_st)

        instance = response_select_st.json()[0].get('instance')
        last_op_id = json.loads(instance).get('lastOpID')

        # Валідація заяви у рішенні
        data_select_decision_reason = [
            {
                "entity": "rrpUb_decisionCard",
                "method": "selectDecisionReason",
                "instance": {
                    "regNum": str(rn_num),
                    "acName": "o_reg",
                    "entityRnNum": None,
                    "limitationID": None,
                    "options": {
                        "isBond": False
                    }
                },
                "formShortcutCode": "NOTAR_RRP_REALTY_CREATE",
                "privCode": "NOTAR_DECISION_OPERATIONS_VIEW"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)2-validatsiya zayavi v rishenni(selectDecisionReason)",
                         headers=self.headers,
                         json=data_select_decision_reason)

        # Додавання інформації з заяви у рішення
        data_select_for_section = [
            {
                "entity": "rrpUb_requestCard",
                "method": "selectForSection",
                "privCode": "NOTAR_REQUEST_OPERATIONS_VIEW",
                "rnNum": str(rn_num)
            }
        ]
        self.client.post("/ubql",
                         name=self.class_name + " (DRRP)2-dodavannya info z zayavi v rishenni(selectForSection)",
                         headers=self.headers,
                         json=data_select_for_section)

        # Реєстрація рішення
        data_check_st_in_decision = [
            {
                "entity": "rrpUb_request",
                "method": "checkRequestRight",
                "shortcutCode": "NOTAR_REQUEST_OPERATIONS",
                "privPrefix": "NOTAR",
                "actionName": "REG_DS",
                "acNameSM": "dcs_register",
                "rnNum": str(rn_num),
                "lastOpID": last_op_id
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)2-perevirka zayavi u rishenni", headers=self.headers,
                         json=data_check_st_in_decision)

        data_create_decision = [
            {
                "entity": "rrpUb_request",
                "method": "dispatchSMEvent",
                "searchParams": "{\"name\":\"dcs_register\",\"operation\":{\"acName\":\"r_rdr\",\"lastOpID\":" + str(
                    last_op_id) + ",\"registrar\":{\"employeeID\":25213,\"regionID\":12091,\"organizationID\":22061},\"opReasonTypeExtension\":\"\",\"decision\":{\"receiveDate\":null,\"termReviewDate\":null,\"dcDsType\":\"14\",\"additional\":\"\",\"partSize\":\"\"},\"subjects\":[{\"ID\":104966375,\"rsbjRsbjID\":null,\"reqReqID\":60885741,\"sbjAdPostalID\":null,\"sbjAdLocationID\":null,\"cdCdID\":null,\"rnRnID\":1256200,\"sbjName\":\"Токар Сергій Володимирович\",\"sbjCode\":null,\"dcCodeAbsenceBit\":\"x0001\",\"dcSbjType\":\"1\",\"isState\":null,\"dcSbjRlNameBit\":\"x11\",\"dcChangeType\":\"2\",\"additional\":null,\"rnNum\":104966375,\"rSubjectRsbjID\":null,\"dcEntityClass\":\"1\",\"reqRnNum\":51230761,\"dcSbjSort\":\"1\",\"dcCountry\":\"225\",\"phone\":null,\"dcSbjAddType\":null,\"sbjPos\":null,\"idEddr\":null,\"isValidated\":0,\"isDmsValidated\":0,\"isNotResident\":null,\"reasonAbsentValidate\":\"рр\",\"surname\":\"Токар\",\"firstName\":\"Сергій\",\"patronymic\":\"Володимирович\",\"taxNumber\":null,\"phoneNumber\":null,\"email\":null,\"isLocalGovernment\":null,\"idDoc\":[{\"ID\":55947198,\"rsbjRsbjID\":104966375,\"rsbjRnNum\":104966375,\"sidTypeExtension\":null,\"publisher\":\"ТЕСТ\",\"seriesNum\":null,\"dcSidType\":\"1\",\"passport\":\"МЕ123454\",\"dcEntityClass\":\"1\",\"docDate\":\"2022-11-01T00:00:00Z\",\"validityDate\":\"2022-07-25T00:00:00Z\",\"sidType\":\"паспорт громадянина України\"}],\"sbjRlName\":\"Заявник; Суб’єкт права\",\"sbjType\":\"фізична особа\",\"codeAbsence\":\"інша причина відсутності коду\",\"country\":\"Україна\"}]},\"instance\":{\"ID\":" + str(
                    id) + ",\"rnNum\":" + str(rn_num) + ",\"dcReqType\":\"19\"}}",
                "privCode": "NOTAR_REQUEST_OPERATIONS_REG_DS"
            }
        ]

        response_create_decision = self.client.post("/ubql", name=self.class_name + " (DRRP)2-stvorennya rishennya",
                                                    headers=self.headers,
                                                    json=data_create_decision)
        search_params = response_create_decision.json()[0].get('searchParams')
        ds_rn_num = json.loads(search_params).get('operation').get('dsRnNum')

        data_generate_pdf_ds_card = [
            {
                "entity": "rrpUb_decisionCard",
                "method": "generateDecisionDoc",
                "privPrefix": "NOTAR",
                "values": "[{\"textareaDisabled\":true,\"textareaValue\":\"РІШЕННЯ\",\"style\":\"header\"},{\"textareaDisabled\":true,\"textareaValue\":\"про державну реєстрацію прав\",\"style\":\"header\"},{\"textareaDisabled\":true,\"textareaValue\":\"№ 63665258\",\"style\":\"additionalHeader\"},{\"textareaDisabled\":true,\"textareaValue\":\"26 листопада 2022 року\",\"style\":\"additionalHeader\"},{\"textareaDisabled\":true,\"style\":\"justify\",\"textareaValue\":\"Державний реєстратор прав на нерухоме майно Панікар Валентина Миколаївна, Києво-Святошинська районна державна нотаріальна контора, Фастівський районний нотаріальний округ, Київська обл.,  розглянувши заяву від 26.11.2022 за реєстраційним номером 51230778 (далі – Заява) відповідно до Закону України «Про державну реєстрацію речових прав на нерухоме майно та їх обтяжень», Порядку державної реєстрації речових прав на нерухоме майно та їх обтяжень, затвердженого постановою Кабінету Міністрів України від 25 грудня 2015 року № 1127,\"},{\"textareaDisabled\":true,\"textareaValue\":\"ВИРІШИВ:\",\"style\":\"normal\"},{\"textareaDisabled\":false,\"textareaValue\":\"Провести державну реєстрацію прав за Заявою.\",\"style\":\"justify\"},{\"textareaDisabled\":true,\"textareaValue\":\"Це рішення може бути оскаржено відповідно до законодавства.\",\"style\":\"normal\"},{\"textareaDisabled\":true,\"tableValues\":[{\"content\":\"Державний реєстратор прав на нерухоме майно\"},{\"content\":\"Валентина ПАНІКАР\"}],\"style\":\"tableSingFooter\",\"textareaValue\":\"\"}]",
                "searchParams": {
                    "acName": "d_get",
                    "rnNum": ds_rn_num
                }
            }
        ]

        generate_pdf_ds_card = self.client.post("/ubql", name=self.class_name + " (DRRP)2-stvorennya DF rishennya",
                                                headers=self.headers,
                                                json=data_generate_pdf_ds_card)
        rep_id = generate_pdf_ds_card.json()[0].get('reportResultID')
        ds_date_time = get_now_strftime("%Y-%m-%dT%H-2:%M:%S.000Z")

        data_sign_pdf_ds_card = [
            {
                "entity": "rep_reportResultSignature",
                "method": "saveSignature",
                "sTime": ds_date_time,
                "execParams": {
                    "repID": rep_id,
                    "signature": "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",
                    "timeStamp": ds_date_time,
                    "serial": self.serial
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)2-pidpisannya DF rishennya", headers=self.headers,
                         json=data_sign_pdf_ds_card)

        # Додовання у рішення дату повідомлення про зупинення розгляду
        data_ds_perform_action = [
            {
                "entity": "rrpUb_decisionCard",
                "method": "performAction",
                "decision": {
                    "rnNum": str(ds_rn_num),
                    "receiveDate": "2023-01-06T00:00:00.000Z"
                },
                "operation": {
                    "acName": "d_mkdt"
                },
                "privCode": "NOTAR_DECISION_OPERATIONS_EDIT_DATE"
            }
        ]
        self.client.post("/ubql",
                         name=self.class_name + " (DRRP)2-dodavannya v rishennya datu pro zupinennya(performAction)",
                         headers=self.headers,
                         json=data_ds_perform_action)

        # Відкриття вкладки розділа
        self.client.post("/ubql", name=self.class_name + " (DRRP)2-vidkrittya vkladki rozdila", headers=self.headers,
                         json=atu_region)

        # Реєстрація розділа
        data_create_onm = [
            {
                "entity": "rrpSec_realtyCard",
                "method": "performAction",
                "instance": "{\"operationData\":{\"registrar\":25213,\"rnNum\":" + str(
                    ds_rn_num) + ",\"reqRnNum\":" + str(
                    rn_num) + ",\"dcEntityChangeTypeBit\":null,\"causeDocuments\":[]},\"realty\":{\"dcReType\":\"1\",\"reType\":\"земельна ділянка\",\"isResidentialBuilding\":null,\"regionID\":10,\"organizationID\":22061,\"isCadNumFromRequest\":true,\"organizationName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"regionName\":\"Київська обл.\",\"isGetFromRequest\":true,\"groundAreaObj\":{},\"fieldsetType\":\"realty\",\"causeDocuments\":[{\"params\":{\"ID\":\"\",\"dcCdKind\":\"12\",\"dcCdType\":\"108\",\"enum\":\"55241385\",\"publisher\":\"Державний земельний кадастр\",\"countPages\":\"\",\"cdTypeExtension\":\"\",\"docDate\":\"2022-11-28T00:00:00.000Z\",\"deliveryDate\":null,\"expirationDate\":null,\"additional\":\"\",\"cdType\":\"відомості з ДЗК\",\"isFilterValid\":true,\"isDabiEcd\":false,\"pagesCount\":1,\"uploadedPages\":1,\"attrReqID\":60885785,\"baseCdID\":338460728,\"baseRnNum\":338460728,\"cdCdID\":null},\"pages\":[{\"ID\":228952536,\"documentID\":355128439,\"pageNumber\":1,\"cdID\":338460728,\"empEmpID\":25213,\"dcCdType\":\"108\",\"addedDate\":\"2022-11-28T18:02:21Z\",\"signature\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"16420018.p7s\\\",\\\"origName\\\":\\\"16420018.p7s\\\",\\\"relPath\\\":\\\"202211/28\\\",\\\"ct\\\":\\\"application/pkcs7-signature\\\",\\\"size\\\":3782,\\\"md5\\\":\\\"15b4facd60c13e33951d1e201c6450ba\\\",\\\"revision\\\":1}\",\"generatedDocument\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"no-file-name.bin\\\",\\\"origName\\\":\\\"no-file-name.bin\\\",\\\"relPath\\\":\\\"202211/28\\\",\\\"ct\\\":\\\"application/octet-stream\\\",\\\"size\\\":58067,\\\"md5\\\":\\\"394d35c512fea114a79f1ae0e8218962\\\",\\\"revision\\\":1}\",\"dcEntityClass\":\"1\",\"entityRnNum\":" + str(
                    rn_num) + "}]}],\"groundArea\":[{\"cadNum\":\"3211200000:09:005:0099\",\"area\":\"0.0366\",\"dcAreaUm\":\"1\"}],\"reLinks\":[],\"realtyParts\":[]}}",
                "operation": "{\"registrar\":25213,\"rnNum\":" + str(ds_rn_num) + ",\"reqRnNum\":" + str(
                    rn_num) + ",\"dcEntityChangeTypeBit\":null,\"causeDocuments\":[],\"acName\":\"o_reg\"}",
                "privCode": "NOTAR_RRP_REALTY_OPERATIONS_CREATE"
            }
        ]

        create_onm = self.client.post("/ubql", name=self.class_name + " (DRRP)2-stvorennya rozdilu",
                                      headers=self.headers,
                                      json=data_create_onm)
        ml_id = create_onm.json()[0].get('message').get('mlID')

        data_create_onm_perform = [
            {
                "entity": "rrpSec_realtyCard",
                "method": "performAction",
                "mlID": ml_id,
                "instance": "{\"operationData\":{\"registrar\":25213,\"rnNum\":" + str(
                    ds_rn_num) + ",\"reqRnNum\":" + str(
                    rn_num) + ",\"dcEntityChangeTypeBit\":null,\"causeDocuments\":[]},\"realty\":{\"dcReType\":\"1\",\"reType\":\"земельна ділянка\",\"isResidentialBuilding\":null,\"regionID\":10,\"organizationID\":22061,\"isCadNumFromRequest\":true,\"organizationName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"regionName\":\"Київська обл.\",\"isGetFromRequest\":true,\"groundAreaObj\":{},\"fieldsetType\":\"realty\",\"causeDocuments\":[{\"params\":{\"ID\":\"\",\"dcCdKind\":\"12\",\"dcCdType\":\"108\",\"enum\":\"55241385\",\"publisher\":\"Державний земельний кадастр\",\"countPages\":\"\",\"cdTypeExtension\":\"\",\"docDate\":\"2022-11-28T00:00:00.000Z\",\"deliveryDate\":null,\"expirationDate\":null,\"additional\":\"\",\"cdType\":\"відомості з ДЗК\",\"isFilterValid\":true,\"isDabiEcd\":false,\"pagesCount\":1,\"uploadedPages\":1,\"attrReqID\":60885785,\"baseCdID\":338460728,\"baseRnNum\":338460728,\"cdCdID\":null},\"pages\":[{\"ID\":228952536,\"documentID\":355128439,\"pageNumber\":1,\"cdID\":338460728,\"empEmpID\":25213,\"dcCdType\":\"108\",\"addedDate\":\"2022-11-28T18:02:21Z\",\"signature\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"16420018.p7s\\\",\\\"origName\\\":\\\"16420018.p7s\\\",\\\"relPath\\\":\\\"202211/28\\\",\\\"ct\\\":\\\"application/pkcs7-signature\\\",\\\"size\\\":3782,\\\"md5\\\":\\\"15b4facd60c13e33951d1e201c6450ba\\\",\\\"revision\\\":1}\",\"generatedDocument\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"no-file-name.bin\\\",\\\"origName\\\":\\\"no-file-name.bin\\\",\\\"relPath\\\":\\\"202211/28\\\",\\\"ct\\\":\\\"application/octet-stream\\\",\\\"size\\\":58067,\\\"md5\\\":\\\"394d35c512fea114a79f1ae0e8218962\\\",\\\"revision\\\":1}\",\"dcEntityClass\":\"1\",\"entityRnNum\":" + str(
                    rn_num) + "}]}],\"groundArea\":[{\"cadNum\":\"3211200000:09:005:0099\",\"area\":\"0.0366\",\"dcAreaUm\":\"1\"}],\"reLinks\":[],\"realtyParts\":[]}}",
                "operation": "{\"registrar\":25213,\"rnNum\":" + str(ds_rn_num) + ",\"reqRnNum\":" + str(
                    rn_num) + ",\"dcEntityChangeTypeBit\":null,\"causeDocuments\":[],\"acName\":\"o_reg\"}",
                "privCode": "NOTAR_RRP_REALTY_OPERATIONS_CREATE"
            }
        ]

        create_onm_perform = self.client.post("/ubql",
                                              name=self.class_name + " (DRRP)2-pidtverdjennya stvorennya rozdilu",
                                              headers=self.headers,
                                              json=data_create_onm_perform)

        reg_num = create_onm_perform.json()[0].get('regNum')

        # Реєстрація ПВ
        data_create_pr = [
            {
                "entity": "rrpSec_propertyCard",
                "method": "performAction",
                "instance": "{\"operationData\":{\"registrar\":25213,\"rnNum\":" + str(
                    ds_rn_num) + ",\"reqRnNum\":" + str(
                    rn_num) + ",\"dcEntityChangeTypeBit\":null,\"causeDocuments\":[]},\"property\":{\"dcPrKind\":\"1\",\"cost\":\"1 000 000,00\",\"dcPrModeBit\":\"x1\",\"subjects\":[{\"sbjName\":\"Кока-Кола\",\"sbjCode\":null,\"dcCodeAbsenceBit\":\"1\",\"dcSbjType\":\"2\",\"cdCdID\":null,\"isState\":0,\"dcChangeType\":\"2\",\"reqReqID\":60885787,\"additional\":null,\"rnNum\":104966447,\"dcEntityClass\":\"6\",\"reqRnNum\":51230800,\"dcSbjSort\":true,\"dcCountry\":18,\"sbjAdLocationID\":null,\"phone\":null,\"sbjAdPostalID\":null,\"dcSbjRlName\":\"11\",\"dcSbjAddType\":null,\"email\":null,\"idEddr\":null,\"isValidated\":0,\"isDmsValidated\":null,\"reasonAbsentValidate\":null,\"surname\":null,\"firstName\":null,\"patronymic\":null,\"taxNumber\":\"111111111111\",\"isNotResident\":1,\"isLocalGovernment\":0,\"idDoc\":[{\"dcEntityClass\":\"6\"}],\"country\":\"Бельгія\"}],\"causeDocuments\":[{\"params\":{\"ID\":\"\",\"dcCdKind\":\"12\",\"dcCdType\":\"108\",\"enum\":\"55241385\",\"publisher\":\"Державний земельний кадастр\",\"countPages\":\"\",\"cdTypeExtension\":\"\",\"docDate\":\"2022-11-28T00:00:00.000Z\",\"deliveryDate\":null,\"expirationDate\":null,\"additional\":\"\",\"cdType\":\"відомості з ДЗК\",\"isFilterValid\":true,\"isDabiEcd\":false,\"pagesCount\":1,\"uploadedPages\":1,\"attrReqID\":60885787,\"baseCdID\":338460733,\"baseRnNum\":338460733,\"cdCdID\":null},\"pages\":[{\"ID\":228952538,\"documentID\":355128442,\"pageNumber\":1,\"cdID\":338460733,\"empEmpID\":25213,\"dcCdType\":\"108\",\"addedDate\":\"2022-11-28T18:42:53Z\",\"signature\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"16420020.p7s\\\",\\\"origName\\\":\\\"16420020.p7s\\\",\\\"relPath\\\":\\\"202211/28\\\",\\\"ct\\\":\\\"application/pkcs7-signature\\\",\\\"size\\\":3782,\\\"md5\\\":\\\"15b4facd60c13e33951d1e201c6450ba\\\",\\\"revision\\\":1}\",\"generatedDocument\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"no-file-name.bin\\\",\\\"origName\\\":\\\"no-file-name.bin\\\",\\\"relPath\\\":\\\"202211/28\\\",\\\"ct\\\":\\\"application/octet-stream\\\",\\\"size\\\":58067,\\\"md5\\\":\\\"394d35c512fea114a79f1ae0e8218962\\\",\\\"revision\\\":1}\",\"dcEntityClass\":\"1\",\"entityRnNum\":" + str(
                    rn_num) + "}]}],\"reRegNum\":" + str(reg_num) + "}}",
                "operation": "{\"registrar\":25213,\"rnNum\":" + str(ds_rn_num) + ",\"reqRnNum\":" + str(
                    rn_num) + ",\"dcEntityChangeTypeBit\":null,\"causeDocuments\":[],\"acName\":\"p_reg\"}",
                "privCode": "NOTAR_RRP_PROPERTY_OPERATIONS_CREATE"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)2-stvorennya prava vlastnosti", headers=self.headers,
                         json=data_create_pr)

    # Пошук заяв
    @task(6)
    def search_st(self):
        data_date = [
            {
                "entity": "rrpUb_requestSearchQuery",
                "method": "search",
                "acName": "r_fnd",
                "searchParams": {
                    "regStartDate": "2021-11-01T00:00:00.000Z",
                    "regFinishDate": "2021-11-30T00:00:00.000Z"
                },
                "privCode": "NOTAR_REQUEST_SEARCH_SIMPLE_SEARCH",
                "privPrefix": "NOTAR"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)3-poshuk zayav za period", headers=self.headers,
                         json=data_date)

    # Пошук рішень
    @task(6)
    def search_ds_date(self):
        data_search = [
            {
                "entity": "rrpUb_decisionCard",
                "method": "search",
                "acName": "d_fnd",
                "searchParams": {
                    "regStartDate": "2021-10-01T00:00:00.000Z",
                    "regFinishDate": "2021-10-31T00:59:59.999Z",
                    "holderObjID": False
                },
                "privCode": "NOTAR_DECISION_OPERATIONS_SEARCH"
            }
        ]
        response_search = self.client.post("/ubql", name=self.class_name + " (DRRP)4-predvar.poshuk rishen za period",
                                           headers=self.headers,
                                           json=data_search)
        sel_id = response_search.get('selID')

        data_search_result = [
            {
                "entity": "rrpUb_decisionCard",
                "method": "searchResult",
                "searchParams": {
                    "selID": sel_id,
                    "total": 78
                },
                "options": {
                    "start": 0,
                    "limit": 78,
                    "page": 1
                },
                "fieldList": [
                    "regNum",
                    "regDate",
                    "dcDsType",
                    "dcDsState",
                    "holderName",
                    "reqRnNum",
                    "holderObjID"
                ]
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)4-poshuk rishen za period(results)",
                         headers=self.headers,
                         json=data_search_result)

    # Черга заяв
    @task(6)
    def queue_st(self):
        data = [
            {
                "entity": "rrpUb_requestSearchQuery",
                "method": "prepareQueue",
                "privPrefix": "NOTAR"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)5-cherga zayav", headers=self.headers, json=data)

    # Пошук заяв БД
    @task(2)
    def search_st_db(self):
        # Пошук за об'єктом (по адресу)
        data_st_db = [
            {
                "entity": "rrpUb_requestSearchQuery",
                "method": "search",
                "acName": "doc_frequest",
                "reason": "",
                "searchParams": {
                    "realty": {
                        "isReAndRepAddressOnly": True,
                        "isNotFull": False,
                        "realtyAddressInfo": {
                            "atuID": 334989
                        }
                    }
                },
                "privCode": "NOTAR_REQUEST_SEARCH_REG_EMPLOYEE"
            }
        ]
        response_st_db = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)6-poshuk zayav v BD", headers=self.headers,
                             json=data_st_db).json()[0]
        result_data = response_st_db.get('resultData')
        search_params = response_st_db.get('searchParams')
        sel_id = response_st_db.get('selID')
        search_time = response_st_db.get('searchTime')

        data_generate_pdf = [
            {
                "entity": "rrpUb_requestSearchQuery",
                "method": "generatePdf",
                "data": result_data,
                "searchParams": search_params,
                "selID": sel_id,
                "reason": "",
                "searchTime": search_time
            }
        ]
        response_generate_pdf = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)6-poshuk zayav v BD (gener PDF)",
                             headers=self.headers,
                             json=data_generate_pdf).json()[0]
        report_result_id = response_generate_pdf.get('reportResultID')

        data_generated_document = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)vidkrittya DF poshuk zayav v BD", headers=self.headers,
        #                 params=data_generated_document)

    # Створення відомості з відкладенним формуванням
    @task(1)
    def vidomosti_za_rezult_poshuku_scheduler(self):
        # Реєстрація Заява про надання інформації (інформація)
        data_create_st_card = [
            {
                "entity": "rrpUb_requestCard",
                "method": "insert",
                "instance": "{\"dcReqType\":\"18\",\"dcDocGiveType\":\"1\",\"dcReqRegType\":\"12\",\"RstCore_EnumCombobox-4886-inputEl\":null,\"outNum\":\"\",\"outDate\":null,\"dcTermReview\":\"7200\",\"termReviewDate\":\"2022-12-04T17:02:00.000Z\",\"extEmail\":\"\",\"dcDocReceiveType\":null,\"additional\":\"\",\"employeeId\":25213,\"reqTypeExtension\":null,\"dcExtReceiveType\":\"2\",\"registrar\":{\"employeeID\":25213,\"regionID\":12091,\"organizationID\":22061},\"dzk\":[],\"paymentDocuments\":[{\"dcPayType\":\"6\",\"enum\":\"8888\",\"rpdDate\":\"2022-11-29T00:00:00.000Z\",\"summ\":\"100,00\",\"orgName\":\"банк\",\"receiptNum\":\"\",\"reportResultID\":\"\",\"dcPdKind\":\"1\",\"payType\":\"Адміністративний збір за надання інформації\",\"ID\":\"\"}],\"subjects\":[{\"idDoc\":[{}],\"dcSbjType\":\"2\",\"dcSbjRlNameBit\":\"\\\"2\\\"\",\"additional\":\"\",\"dcCodeAbsenceBit\":\"x1\",\"isState\":\"0\",\"dcSbjAddType\":\"2\",\"dcCountry\":233,\"dcSbjSort\":\"1\",\"isNotResident\":true,\"phone\":\"\",\"phoneNumber\":\"\",\"email\":\"\",\"taxNumber\":\"111111111111\",\"sbjName\":\"Кока-Кола\",\"isLocalGovernment\":false,\"isValidated\":\"0\",\"exchEdrID\":null,\"ID\":null,\"authorized\":{\"idDoc\":[{\"dcSidType\":null,\"docDate\":null,\"seriesNum\":\"\",\"publisher\":null,\"sidTypeExtension\":null,\"validityDate\":null}],\"dcSbjType\":\"1\",\"additional\":\"\",\"dcCountry\":225,\"causeDocument\":{\"docDate\":\"2022-11-29T00:00:00.000Z\",\"docTypeUser\":\"Паспорт\",\"enum\":\"ААО 948566\",\"publisher\":\"ДВС\"},\"email\":\"\",\"firstName\":\"Тест\",\"idEddr\":\"\",\"patronymic\":\"Тестович\",\"phone\":\"\",\"phoneNumber\":\"\",\"sbjCode\":\"4545545554\",\"sbjName\":\"Тестовий  Тест Тестович\",\"sbjPos\":null,\"surname\":\"Тестовий \",\"isValidated\":\"0\",\"isDmsValidated\":\"0\",\"ID\":null,\"dcSbjSort\":\"2\"}}],\"causeDocuments\":[],\"realties\":[],\"filter\":{\"address\":{},\"subject\":{\"dcSbjType\":\"2\",\"sbjCode\":\"39792822\"},\"isSubjectExists\":true},\"body\":{\"dcReqDocType\":\"6\",\"dcDocTypeInfo\":\"2\",\"dcDocReqType\":\"1\",\"startDate\":null,\"finishDate\":null,\"dcReqTypeSubject\":\"2\",\"isOwner\":null,\"dcEntityChangeTypeBit\":\"x0001\"}}",
                "operation": "{\"acName\":\"r_reg\",\"registrar\":{}}",
                "privCode": "NOTAR_REQUEST_OPERATIONS_INPUT"
            }
        ]

        response_create_st_card = self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya zayavi",
                                                   headers=self.headers, json=data_create_st_card).json()[0]
        rn_num = response_create_st_card.get('rnNum')
        id = response_create_st_card.get('ID')
        req_save_info = response_create_st_card.get('reqSaveInfo')
        op_date = json.loads(req_save_info).get('opDate')

        data_generate_pdf_st_card = [
            {
                "entity": "rrpUb_requestSearch",
                "method": "generatePdf",
                "requestInfoRecord": {
                    "ID": id,
                    "rnNum": rn_num,
                    "regNum": rn_num,
                    "dcReqType": "18",
                    "dcReqRegType": "12",
                    "causeDocuments": "[]",
                    "regDate": op_date,
                    "holderObjID": 22061
                },
                "repReportResultID": None,
                "privPrefix": "NOTAR",
                "operation": "RequestPdf"
            }
        ]
        response_generate_pdf_st_card = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya DF zayavi", headers=self.headers,
                             json=data_generate_pdf_st_card).json()[0]
        report_result_id_generate_st_pdf = response_generate_pdf_st_card.get('reportResultID')

        data_get_doc_st_pdf = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id_generate_st_pdf,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id_generate_st_pdf),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id_generate_st_pdf)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)vidkrittaya DF zayavi", headers=self.headers,
        #                 params=data_get_doc_st_pdf)

        # Пошук (запит тяжкий, суб'єкт має 16325 об'єктів виконується 1хв 44с)
        data_search = [
            {
                "entity": "rrpScheduler_infoRrp",
                "method": "saveQueueTask",
                "searchParams": {
                    "reasonParameters": {
                        "regNum": str(rn_num),
                        "additional": "Автотест",
                        "docTypeInfo": "2",
                        "isChanges": True,
                        "isShowHistoricalNames": True,
                        "rrpRegistries": {
                            "allRrpRegisters": "on",
                            "properties": "1",
                            "irps": "2",
                            "mortgage": "3",
                            "limitation": "4",
                            "bRealty": "5"
                        },
                        "oldRegistries": {
                            "allOldRrpRegisters": "on",
                            "oldRealty": "1",
                            "oldLimitation": "2",
                            "oldMortgage": "3"
                        },
                        "employeeId": 25213,
                        "employeeInfo": {
                            "employeeName": "Панікар Валентина Миколаївна",
                            "ercObjName": "Києво-Святошинська районна державна нотаріальна контора Фастівський районний нотаріальний округ ",
                            "ercAtuName": "Київська обл."
                        }
                    },
                    "extractParameters": {
                        "subjectSearchInfo": {
                            "sbjCode": "39792822",
                            "dcSearchAlgorithm": "2",
                            "addressType": "1"
                        },
                        "searchBy": "1"
                    },
                    "searchByP": {
                        "searchBy": 1
                    },
                    "searchInfo": {},
                    "reportResultID": None,
                    "dcDocType": "21"
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)7-vidomosti za rezult poshuku (scheduler)",
                         headers=self.headers,
                         json=data_search)

    # Створення відомості
    @task(3)
    def vidomosti_za_rezult_poshuku(self):
        # Реєстрація Заява про надання інформації (інформація)
        data_create_st_card = [
            {
                "entity": "rrpUb_requestCard",
                "method": "insert",
                "instance": "{\"dcReqType\":\"18\",\"dcDocGiveType\":\"1\",\"dcReqRegType\":\"12\",\"RstCore_EnumCombobox-4886-inputEl\":null,\"outNum\":\"\",\"outDate\":null,\"dcTermReview\":\"7200\",\"termReviewDate\":\"2022-12-04T17:02:00.000Z\",\"extEmail\":\"\",\"dcDocReceiveType\":null,\"additional\":\"\",\"employeeId\":25213,\"reqTypeExtension\":null,\"dcExtReceiveType\":\"2\",\"registrar\":{\"employeeID\":25213,\"regionID\":12091,\"organizationID\":22061},\"dzk\":[],\"paymentDocuments\":[{\"dcPayType\":\"6\",\"enum\":\"8888\",\"rpdDate\":\"2022-11-29T00:00:00.000Z\",\"summ\":\"100,00\",\"orgName\":\"банк\",\"receiptNum\":\"\",\"reportResultID\":\"\",\"dcPdKind\":\"1\",\"payType\":\"Адміністративний збір за надання інформації\",\"ID\":\"\"}],\"subjects\":[{\"idDoc\":[{}],\"dcSbjType\":\"2\",\"dcSbjRlNameBit\":\"\\\"2\\\"\",\"additional\":\"\",\"dcCodeAbsenceBit\":\"x1\",\"isState\":\"0\",\"dcSbjAddType\":\"2\",\"dcCountry\":233,\"dcSbjSort\":\"1\",\"isNotResident\":true,\"phone\":\"\",\"phoneNumber\":\"\",\"email\":\"\",\"taxNumber\":\"111111111111\",\"sbjName\":\"Кока-Кола\",\"isLocalGovernment\":false,\"isValidated\":\"0\",\"exchEdrID\":null,\"ID\":null,\"authorized\":{\"idDoc\":[{\"dcSidType\":null,\"docDate\":null,\"seriesNum\":\"\",\"publisher\":null,\"sidTypeExtension\":null,\"validityDate\":null}],\"dcSbjType\":\"1\",\"additional\":\"\",\"dcCountry\":225,\"causeDocument\":{\"docDate\":\"2022-11-29T00:00:00.000Z\",\"docTypeUser\":\"Паспорт\",\"enum\":\"ААО 948566\",\"publisher\":\"ДВС\"},\"email\":\"\",\"firstName\":\"Тест\",\"idEddr\":\"\",\"patronymic\":\"Тестович\",\"phone\":\"\",\"phoneNumber\":\"\",\"sbjCode\":\"4545545554\",\"sbjName\":\"Тестовий  Тест Тестович\",\"sbjPos\":null,\"surname\":\"Тестовий \",\"isValidated\":\"0\",\"isDmsValidated\":\"0\",\"ID\":null,\"dcSbjSort\":\"2\"}}],\"causeDocuments\":[],\"realties\":[],\"filter\":{\"address\":{},\"subject\":{\"dcSbjType\":\"2\",\"sbjCode\":\"39792822\"},\"isSubjectExists\":true},\"body\":{\"dcReqDocType\":\"6\",\"dcDocTypeInfo\":\"2\",\"dcDocReqType\":\"1\",\"startDate\":null,\"finishDate\":null,\"dcReqTypeSubject\":\"2\",\"isOwner\":null,\"dcEntityChangeTypeBit\":\"x0001\"}}",
                "operation": "{\"acName\":\"r_reg\",\"registrar\":{}}",
                "privCode": "NOTAR_REQUEST_OPERATIONS_INPUT"
            }
        ]

        response_create_st_card = self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya zayavi",
                                                   headers=self.headers, json=data_create_st_card).json()[0]
        rn_num = response_create_st_card.get('rnNum')
        id = response_create_st_card.get('ID')
        req_save_info = response_create_st_card.get('reqSaveInfo')
        op_date = json.loads(req_save_info).get('opDate')

        data_generate_pdf_st_card = [
            {
                "entity": "rrpUb_requestSearch",
                "method": "generatePdf",
                "requestInfoRecord": {
                    "ID": id,
                    "rnNum": rn_num,
                    "regNum": rn_num,
                    "dcReqType": "18",
                    "dcReqRegType": "12",
                    "causeDocuments": "[]",
                    "regDate": op_date,
                    "holderObjID": 22061
                },
                "repReportResultID": None,
                "privPrefix": "NOTAR",
                "operation": "RequestPdf"
            }
        ]
        response_generate_pdf_st_card = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya DF zayavi", headers=self.headers,
                             json=data_generate_pdf_st_card).json()[0]
        report_result_id_generate_st_pdf = response_generate_pdf_st_card.get('reportResultID')

        data_get_doc_st_pdf = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id_generate_st_pdf,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id_generate_st_pdf),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id_generate_st_pdf)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)vidkrittaya DF zayavi", headers=self.headers,
        #                 params=data_get_doc_st_pdf, debug_stream=sys.stderr)

        # Перевірка заяви на валідність
        data_get_request_short_info = [
            {
                "entity": "rrpUb_request",
                "method": "getRequestShortInfo",
                "privCode": "NOTAR_REQUEST_OPERATIONS_VIEW",
                "queryParameters": {
                    "rnNum": str(rn_num),
                    "actionName": "consolidatedExtract"
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)perevirka zayavi validatsiya(getRequestShortInfo)",
                         headers=self.headers,
                         json=data_get_request_short_info)

        # Пошук (суб'єкт декілька об'єктів)
        data_search = [
            {
                "entity": "rrpUb_extractRrp",
                "method": "search",
                "searchParams": {
                    "reasonParameters": {
                        "regNum": str(rn_num),
                        "docTypeInfo": "2",
                        "isChanges": True,
                        "isShowHistoricalNames": True,
                        "rrpRegistries": {
                            "allRrpRegisters": "on",
                            "properties": "1",
                            "irps": "2",
                            "mortgage": "3",
                            "limitation": "4",
                            "bRealty": "5"
                        },
                        "oldRegistries": {
                            "allOldRrpRegisters": "on",
                            "oldRealty": "1",
                            "oldLimitation": "2",
                            "oldMortgage": "3"
                        },
                        "employeeId": 25213,
                        "employeeInfo": {
                            "employeeName": "Панікар Валентина Миколаївна",
                            "ercObjName": "Києво-Святошинська районна державна нотаріальна контора Фастівський районний нотаріальний округ ",
                            "ercAtuName": "Київська обл."
                        }
                    },
                    "extractParameters": {
                        "subjectSearchInfo": {
                            "sbjCode": "33261467",
                            "dcSearchAlgorithm": "2",
                            "addressType": "1"
                        },
                        "searchBy": "1"
                    },
                    "searchByP": {
                        "searchBy": 1
                    },
                    "searchInfo": {},
                    "reportResultID": None,
                    "dcDocType": "21"
                }
            }
        ]
        response_search = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)8-vidomosti za rezult poshuku",
                             headers=self.headers,
                             json=data_search).json()[0]
        search_info = json.loads(response_search.get('resultData')).get('searchInfo')
        report_result_temp_id = search_info.get('reportResultTempID')
        search_id = search_info.get('searchID')
        date = search_info.get('date')

        data_generate_pdf_vidomosti = [
            {
                "entity": "rrpUb_extractRrp",
                "method": "generatePdf",
                "searchParams": {
                    "reasonParameters": {
                        "regNum": str(rn_num),
                        "docTypeInfo": "2",
                        "isChanges": True,
                        "isShowHistoricalNames": True,
                        "rrpRegistries": {
                            "allRrpRegisters": "on",
                            "properties": "1",
                            "irps": "2",
                            "mortgage": "3",
                            "limitation": "4",
                            "bRealty": "5"
                        },
                        "oldRegistries": {
                            "allOldRrpRegisters": "on",
                            "oldRealty": "1",
                            "oldLimitation": "2",
                            "oldMortgage": "3"
                        },
                        "employeeId": 25213,
                        "employeeInfo": {
                            "employeeName": "Панікар Валентина Миколаївна",
                            "ercObjName": "Києво-Святошинська районна державна нотаріальна контора Фастівський районний нотаріальний округ ",
                            "ercAtuName": "Київська обл."
                        }
                    },
                    "extractParameters": {
                        "subjectSearchInfo": {
                            "sbjCode": "33261467",
                            "dcSearchAlgorithm": "2",
                            "addressType": "1"
                        },
                        "searchBy": "1"
                    },
                    "searchByP": {
                        "searchBy": 1
                    },
                    "searchInfo": {
                        "reportResultTempID": report_result_temp_id,
                        "searchID": search_id,
                        "date": date,
                        "employee": "Панікар Валентина Миколаївна, Києво-Святошинська районна державна нотаріальна контора, Фастівський районний нотаріальний округ, Київська обл.",
                        "employeeCurrent": "Панікар Валентина Миколаївна",
                        "addressInfoString": ""
                    },
                    "reportResultID": None,
                    "dcDocType": "21"
                }
            }
        ]
        response_generate_pdf_vidomosti = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)8-stvorennya DF vidomosti za rezult poshuku ",
                             headers=self.headers,
                             json=data_generate_pdf_vidomosti).json()[0]
        report_result_id_generate_vidomosti_pdf = response_generate_pdf_vidomosti.get('reportResultID')

        data_get_doc_vidomosti_pdf = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id_generate_vidomosti_pdf,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id_generate_vidomosti_pdf),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id_generate_vidomosti_pdf)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)vidkrittaya DF vidomosti za rezult poshuku", headers=self.headers,
        #                 params=data_get_doc_vidomosti_pdf)

    # Створення виписка
    @task(1)
    def create_vipiska(self):
        # Реєстрація Заява про надання інформації (виписка)
        data_create_st_card = [
            {
                "entity": "rrpUb_requestCard",
                "method": "insert",
                "instance": "{\"dcReqType\":\"18\",\"dcDocGiveType\":\"1\",\"dcReqRegType\":\"12\",\"RstCore_EnumCombobox-3552-inputEl\":null,\"outNum\":\"\",\"outDate\":null,\"dcTermReview\":\"7200\",\"termReviewDate\":\"2022-12-05T15:30:00.000Z\",\"extEmail\":\"\",\"dcDocReceiveType\":null,\"additional\":\"\",\"employeeId\":25213,\"reqTypeExtension\":null,\"dcExtReceiveType\":\"2\",\"registrar\":{\"employeeID\":25213,\"regionID\":12091,\"organizationID\":22061},\"dzk\":[],\"paymentDocuments\":[{\"dcPayType\":\"5\",\"enum\":\"8888\",\"rpdDate\":\"2022-11-30T00:00:00.000Z\",\"summ\":\"100,00\",\"orgName\":\"банк\",\"receiptNum\":\"\",\"reportResultID\":\"\",\"dcPdKind\":\"1\",\"payType\":\"Адміністративний збір за реєстраційні дії\"}],\"subjects\":[{\"idDoc\":[{\"rsbjRsbjID\":null,\"dcSidType\":null}],\"dcSbjType\":\"2\",\"dcSbjRlNameBit\":[\"2\"],\"dcSbjSort\":\"1\",\"dcCodeAbsenceBit\":\"x1\",\"ID\":null,\"rsbjRsbjID\":null,\"reqReqID\":null,\"sbjAdPostalID\":null,\"sbjAdLocationID\":null,\"cdCdID\":null,\"rnRnID\":null,\"sbjName\":\"Кока-Кола\",\"isState\":\"0\",\"dcChangeType\":\"2\",\"additional\":null,\"rnNum\":null,\"rSubjectRsbjID\":null,\"dcEntityClass\":\"1\",\"reqRnNum\":null,\"dcCountry\":233,\"phone\":null,\"dcSbjAddType\":\"2\",\"sbjPos\":null,\"idEddr\":null,\"isValidated\":\"0\",\"isDmsValidated\":\"0\",\"isNotResident\":1,\"reasonAbsentValidate\":null,\"surname\":null,\"firstName\":null,\"patronymic\":null,\"taxNumber\":\"111111111111\",\"phoneNumber\":null,\"email\":null,\"isLocalGovernment\":0,\"authorized\":{\"idDoc\":[{\"rsbjRsbjID\":null,\"dcSidType\":null}],\"dcSbjType\":\"1\",\"causeDocument\":{\"ID\":338461506,\"dcCdSort\":\"4\",\"dcCdType\":\"60\",\"publisher\":\"ДВС\",\"enum\":\"ААО 948566\",\"dcChangeType\":\"2\",\"docTypeUser\":\"Паспорт\",\"rnNum\":338461506,\"dcEntityClass\":\"1\",\"docDate\":\"29.11.2022\",\"cdType\":\"документ уповноваженної особи\"},\"ID\":null,\"rsbjRsbjID\":null,\"reqReqID\":60886028,\"sbjAdPostalID\":null,\"sbjAdLocationID\":null,\"cdCdID\":338461506,\"rnRnID\":null,\"sbjName\":\"Тестовий  Тест Тестович\",\"sbjCode\":\"4545545554\",\"isState\":null,\"dcChangeType\":\"2\",\"additional\":null,\"rnNum\":null,\"rSubjectRsbjID\":104966924,\"dcEntityClass\":\"1\",\"reqRnNum\":51231039,\"dcCountry\":225,\"phone\":null,\"dcSbjAddType\":null,\"sbjPos\":null,\"idEddr\":null,\"isValidated\":\"0\",\"isDmsValidated\":\"0\",\"isNotResident\":null,\"reasonAbsentValidate\":null,\"surname\":\"Тестовий \",\"firstName\":\"Тест\",\"patronymic\":\"Тестович\",\"taxNumber\":null,\"phoneNumber\":null,\"email\":null,\"isLocalGovernment\":null,\"dcSbjSort\":\"2\"}}],\"causeDocuments\":[],\"realties\":[],\"filter\":{\"address\":{},\"subject\":{\"dcSbjType\":\"2\",\"sbjCode\":\"39792822\"},\"isSubjectExists\":true},\"body\":{\"dcReqDocType\":\"2\",\"dcDocTypeInfo\":null,\"dcDocReqType\":\"1\",\"startDate\":\"2022-11-30T00:00:00.000Z\",\"finishDate\":\"2022-11-30T00:00:00.000Z\",\"dcReqTypeSubject\":\"2\",\"isOwner\":null,\"dcEntityChangeTypeBit\":null}}",
                "operation": "{\"acName\":\"r_reg\",\"registrar\":{}}",
                "privCode": "NOTAR_REQUEST_OPERATIONS_INPUT"
            }
        ]
        response_create_st_card = self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya zayavi",
                                                   headers=self.headers, json=data_create_st_card).json()[0]
        rn_num = response_create_st_card.get('rnNum')
        id = response_create_st_card.get('ID')
        req_save_info = response_create_st_card.get('reqSaveInfo')
        op_date = json.loads(req_save_info).get('opDate')

        data_generate_pdf_st_card = [
            {
                "entity": "rrpUb_requestSearch",
                "method": "generatePdf",
                "requestInfoRecord": {
                    "ID": id,
                    "rnNum": rn_num,
                    "regNum": rn_num,
                    "dcReqType": "18",
                    "dcReqRegType": "12",
                    "causeDocuments": "[]",
                    "regDate": op_date,
                    "holderObjID": 22061
                },
                "repReportResultID": None,
                "privPrefix": "NOTAR",
                "operation": "RequestPdf"
            }
        ]
        response_generate_pdf_st_card = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya DF zayavi", headers=self.headers,
                             json=data_generate_pdf_st_card).json()[0]
        report_result_id_generate_st_pdf = response_generate_pdf_st_card.get('reportResultID')

        data_get_doc_st_pdf = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id_generate_st_pdf,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id_generate_st_pdf),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id_generate_st_pdf)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)vidkrittaya DF zayavi", headers=self.headers,
        #                 params=data_get_doc_st_pdf, debug_stream=sys.stderr)

        # Пошук
        data_search = [
            {
                "entity": "rrpDoc_excerpt",
                "method": "search",
                "searchParams": {
                    "realty": None,
                    "requestRegNum": "51231083",
                    "additional": None,
                    "startDate": "2016-01-01T00:00:00.000Z",
                    "finishDate": "2021-12-31T23:59:59.999Z",
                    "registrarEmpID": 25213,
                    "subject": {
                        "sbjCode": "39792822",
                        "seriesNum": "",
                        "sbjType": "2",
                        "idEddr": "",
                        "sbjName": ""
                    }
                }
            }
        ]
        response_search = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)9-poshuk vipiska", headers=self.headers,
                             json=data_search).json()[0]
        report_result_temp_id = json.loads(response_search.get('resultData')).get('reportResultTempID')

        data_generate_pdf_vipiska = [
            {
                "entity": "rrpDoc_excerpt",
                "method": "generatePdf",
                "reportResultTempID": report_result_temp_id
            }
        ]
        response_generate_pdf_vipiska = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)9-stvorennya DF vipiski", headers=self.headers,
                             json=data_generate_pdf_vipiska).json()[0]

        report_result_id_generate_vipiska_pdf = response_generate_pdf_vipiska.get('reportResultID')

        data_get_doc_vipiska_pdf = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id_generate_vipiska_pdf,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id_generate_vipiska_pdf),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id_generate_vipiska_pdf)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)vidkrittaya DF vipiski", headers=self.headers,
        #                 params=data_get_doc_vipiska_pdf, debug_stream=sys.stderr)

    # Створення витягу
    @task(2)
    def create_vityag(self):
        data_search = [
            {
                "entity": "rrpDoc_extractRrp",
                "method": "search",
                "searchParams": {
                    "reasonParameters": {
                        "docType": "1",
                        "regNum": "46510382",
                        "isShowHistoricalNames": True,
                        "additional": "Автотест",
                        "employeeId": 25213,
                        "rrpRegistries": {
                            "properties": "1"
                        },
                        "oldRegistries": {},
                        "employeeInfo": {
                            "employeeName": "Панікар Валентина Миколаївна",
                            "ercObjName": "Києво-Святошинська районна державна нотаріальна контора Фастівський районний нотаріальний округ ",
                            "ercAtuName": "Київська обл."
                        },
                        "prNum": 42762567,
                        "prNumType": "1",
                        "searchBy": "3"
                    },
                    "extractParameters": {},
                    "searchInfo": {
                        "reportResultTempID": None,
                        "searchID": 708347111,
                        "date": "2022-11-30T18:44:21.712Z",
                        "employee": "Панікар Валентина Миколаївна, Києво-Святошинська районна державна нотаріальна контора, Фастівський районний нотаріальний округ, Київська обл.",
                        "employeeCurrent": "Панікар В.М.",
                        "addressInfoString": ""
                    },
                    "reportResultID": None,
                    "requestRegNum": "46510382"
                }
            }
        ]
        response_search = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)10-poshuk vityag", headers=self.headers,
                             json=data_search).json()[0]
        search_info = json.loads(response_search.get('resultData')).get('searchInfo')
        report_result_temp_id = search_info.get('reportResultTempID')
        search_id = search_info.get('searchID')
        date = search_info.get('date')

        data_generate_pdf = [
            {
                "entity": "rrpDoc_extractRrp",
                "method": "generatePdf",
                "searchParams": {
                    "reasonParameters": {
                        "docType": "1",
                        "regNum": "46510382",
                        "isShowHistoricalNames": True,
                        "additional": "Автотест",
                        "employeeId": 25213,
                        "rrpRegistries": {
                            "properties": "1"
                        },
                        "oldRegistries": {},
                        "employeeInfo": {
                            "employeeName": "Панікар Валентина Миколаївна",
                            "ercObjName": "Києво-Святошинська районна державна нотаріальна контора Фастівський районний нотаріальний округ ",
                            "ercAtuName": "Київська обл."
                        },
                        "prNum": 42762567,
                        "prNumType": "1",
                        "searchBy": "3"
                    },
                    "extractParameters": {},
                    "searchInfo": {
                        "reportResultTempID": report_result_temp_id,
                        "searchID": search_id,
                        "date": date,
                        "employee": "Панікар Валентина Миколаївна, Києво-Святошинська районна державна нотаріальна контора, Фастівський районний нотаріальний округ, Київська обл.",
                        "employeeCurrent": "Панікар В.М.",
                        "addressInfoString": ""
                    },
                    "reportResultID": None,
                    "requestRegNum": "46510382"
                }
            }
        ]
        response_generate_pdf = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)10-stvorennya DF vityag", headers=self.headers,
                             json=data_generate_pdf).json()[0]
        report_result_id_generate_vityag_pdf = response_generate_pdf.get('reportResultID')

        data_get_doc_vityag_pdf = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id_generate_vityag_pdf,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id_generate_vityag_pdf),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id_generate_vityag_pdf)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)vidkrittaya DF vipiski", headers=self.headers,
        #                 params=data_get_doc_vityag_pdf, debug_stream=sys.stderr)

    # Створення інфодовідки
    @task(3)
    def create_infospravka_sbj(self):
        data_generate = [
            {
                "entity": "rrpUb_infoRrp",
                "method": "generate",
                "searchParams": {
                    "isShowHistoricalNames": False,
                    "searchType": "2",
                    "reason": "Автотест",
                    "isSuspend": False,
                    "dcReqtypeSubject": "4",
                    "subjectSearchInfo": {
                        "sbjType": "2",
                        "sbjCode": "39792822",
                        "dcSearchAlgorithm": "1"
                    },
                    "employeeId": 25213
                }
            }
        ]
        response_generate = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)12-Infospravka poshuk po sbj",
                             headers=self.headers,
                             json=data_generate).json()[0]
        result_data = json.loads(response_generate.get('resultData'))
        report_result_id = result_data.get('reportResultID')
        group_result_id = result_data.get('groupResult')[0].get('ID')

        data_generate_pdf = [
            {
                "entity": "rrpUb_infoRrp",
                "method": "generatePdf",
                "resultData": None,
                "reportResultID": report_result_id,
                "groupID": group_result_id
            }
        ]
        response_generate_pdf = \
            self.client.post("/ubql", name=self.class_name + " (DRRP)12-stvorennya DF infospravki",
                             headers=self.headers,
                             json=data_generate_pdf).json()[0]
        report_result_id_generate_pdf = response_generate_pdf.get('reportResultID')

        data_get_doc_pdf = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id_generate_pdf,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id_generate_pdf),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id_generate_pdf)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)12-vidkrittaya DF infospravki", headers=self.headers,
        #                 params=data_get_doc_pdf, debug_stream=sys.stderr)

    # Створення інфодовідки з відкладенним формуванням:
    @task(1)
    def create_infospravka_sbj_scheduler(self):
        data_save_queue_task = [
            {
                "entity": "rrpScheduler_infoRrp",
                "method": "saveQueueTask",
                "searchParams": {
                    "isShowHistoricalNames": False,
                    "searchType": "2",
                    "reason": "Автотест",
                    "isSuspend": False,
                    "dcReqtypeSubject": "4",
                    "subjectSearchInfo": {
                        "generalSubjectSearch": True,
                        "sbjType": "2",
                        "sbjName": "ДТЕК",
                        "dcSearchAlgorithm": "1"
                    },
                    "employeeId": 25213,
                    "dcDocType": "13"
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)infospravka (scheduler)", headers=self.headers,
                         json=data_save_queue_task)

    # Додано 2 метода erc_employee та erc_object_atu. Методи додають атрибути у форми при відкритті.
    # Приклад на форму відкриття заяви
    @task(10)
    def open_tag(self):
        # Відкриття вкладки
        self.client.post("/ubql", name=self.class_name + " (DRRP)Vidkrittya vklsdki(erc_employee)",
                         headers=self.headers,
                         json=erc_employee)
        self.client.post("/ubql", name=self.class_name + " (DRRP)Vidkrittya vklsdki(erc_object_atu)",
                         headers=self.headers,
                         json=erc_object_atu)

    @task(5)
    def get_data_from_atu(self):
        # Отримання даних АТУ
        self.client.post("/ubql", name=self.class_name + " (DRRP)Otrimannya danih atu(atu_atu_locality)",
                         headers=self.headers,
                         json=atu_atu_locality)
        self.client.post("/ubql", name=self.class_name + " (DRRP)Otrimannya danih atu(atu_atu_object)",
                         headers=self.headers,
                         json=atu_atu_object)
        self.client.post("/ubql", name=self.class_name + " (DRRP)Otrimannya danih atu(atu_atu_street)",
                         headers=self.headers,
                         json=atu_atu_street)

    @task
    def search_info_to_2013(self):
        # Пошук архівних записів
        data = [
            {
                "entity": "rrpOld_search",
                "method": "search",
                "searchParams": {
                    "objectSearchInfo": {
                        "realtyAddressInfo": {
                            "streetAtuId": 331537,
                            "localityAtuId": "26",
                            "houseType": "1",
                            "house": "23",
                            "isReAddressOnly": None,
                            "isRepAddressOnly": None
                        }
                    },
                    "searchBy": "1",
                    "dcSearchRegistryTypes": "2"
                },
                "privPrefix": "NOTAR"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)poshuk arhiv zapisiv(rrpOld_search)",
                         headers=self.headers,
                         json=data)

    @task
    def transfer_of_rights_to_process(self):
        # Передача прав на обробку заяв та запитів
        # Реєстрація заяви ПВ
        data_create_st_card = json.loads(
            get_text_from_file(os.path.abspath('./data/data_create_st_card.txt')))
        response_create_st_card = self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya zayavi",
                                                   headers=self.headers,
                                                   json=data_create_st_card)
        rn_num = response_create_st_card.json()[0].get('rnNum')
        id = response_create_st_card.json()[0].get('ID')

        data_generate_pdf_st_card = [
            {
                "entity": "rrpUb_requestSearch",
                "method": "generatePdf",
                "requestInfoRecord": "{\"ID\":" + str(id) + ",\"reqReqID\":null,\"rnNum\":" + str(
                    rn_num) + ",\"dcReqState\":\"6\",\"holderObjID\":22061,\"holderObjnID\":4367,\"reqTypeExtension\":null,\"signDate\":null,\"outNum\":\"1\",\"senderEmpID\":null,\"formatVersion\":2,\"receiverObjID\":null,\"receiverObjnID\":null,\"regDate\":\"2022-11-23T23:22:37Z\",\"reqCode\":null,\"additional\":\"API\",\"senderObjID\":null,\"senderObjnID\":null,\"createDate\":null,\"receiverAtuID\":null,\"dcReqType\":\"19\",\"dcReqRegType\":\"1\",\"regNum\":\"51230684\",\"isActual\":\"1\",\"senderAtuID\":null,\"dcReqSort\":\"2\",\"holderAtuID\":10,\"dcDocReceiveType\":null,\"outDate\":\"2022-11-22T00:00:00Z\",\"rrbRrbID\":58601996,\"sendDate\":null,\"transferDate\":null,\"mi_wfState\":\"6\",\"dcDocGiveType\":\"1\",\"isReducedTerm\":null,\"dcExtReceiveType\":\"2\",\"extEmail\":null,\"dcTermReview\":\"7200\",\"dcApproveState\":4,\"termReviewDate\":\"2022-11-28T23:22:00Z\",\"body\":{\"ID\":58601996,\"isPrLimited\":null,\"rbDescription\":null,\"enum\":null,\"enumIrp\":null,\"enumPr\":null,\"dcDocTypeInfo\":null,\"entityLastOpID\":null,\"dcPrCommonKind\":null,\"lmTypeExtension\":null,\"decEnum\":null,\"enumReq\":null,\"dcReqDocType\":null,\"descriptionLmObject\":null,\"dcPrType\":null,\"additional\":null,\"changesDescription\":null,\"dcRecType\":null,\"rnNumBrealty\":null,\"irpPrTypeExtension\":null,\"isUndefined\":null,\"dcCourtDecision\":null,\"isExtractNeed\":null,\"dcCancelKind\":null,\"enumRealty\":null,\"dcDocReqType\":null,\"rnNumRealty\":null,\"dcIrpSortReq\":null,\"dcLmType\":null,\"dcEnumType\":null,\"series\":null,\"num\":null,\"enumBrealty\":null,\"dcEntityChangeTypeBit\":\"x000001\",\"isOwner\":null,\"dcReqTypeSubject\":null,\"startDate\":null,\"finishDate\":null,\"cadNum\":null,\"dcPrKind\":\"1\",\"dcEasementType\":null,\"easementTypeExtension\":null,\"isContractEmphyteutist\":null,\"dcSearchType\":null,\"dcErrorType\":null,\"dcRecTypeLnkTo\":null,\"entityChangeTypeBit\":\"набуття\",\"docTypeInfo\":\"<не вказано>\",\"prKind\":\"право власності\"},\"subjects\":[{\"ID\":104966297,\"rsbjRsbjID\":null,\"reqReqID\":60885663,\"sbjAdPostalID\":null,\"sbjAdLocationID\":null,\"cdCdID\":null,\"rnRnID\":13134294,\"sbjName\":\"КІЛЮХ РАНІЛЬ ЄСЕЙОВИЧ\",\"sbjCode\":\"2564489755\",\"dcCodeAbsenceBit\":null,\"dcSbjType\":\"1\",\"isState\":null,\"dcSbjRlNameBit\":\"x11\",\"dcChangeType\":\"2\",\"additional\":null,\"rnNum\":104966297,\"rSubjectRsbjID\":null,\"dcEntityClass\":\"1\",\"reqRnNum\":51230684,\"dcSbjSort\":\"1\",\"dcCountry\":\"225\",\"phone\":null,\"dcSbjAddType\":null,\"sbjPos\":null,\"idEddr\":null,\"isValidated\":1,\"isDmsValidated\":0,\"isNotResident\":null,\"reasonAbsentValidate\":null,\"surname\":\"КІЛЮХ\",\"firstName\":\"РАНІЛЬ\",\"patronymic\":\"ЄСЕЙОВИЧ\",\"taxNumber\":null,\"phoneNumber\":null,\"email\":null,\"isLocalGovernment\":null,\"sbjRlName\":\"Заявник; Суб’єкт права\",\"sbjType\":\"фізична особа\",\"country\":\"Україна\"}],\"realties\":[{\"ID\":54020835,\"rreRreID\":null,\"reqReqID\":60885663,\"reSubTypeExtension\":null,\"sbjCode\":null,\"sbjName\":null,\"enum\":null,\"dcChangeType\":\"2\",\"dcReType\":\"1\",\"dcReTypeOnm\":\"1\",\"description\":null,\"reqRnNum\":51230684,\"isFewAreaLoc\":null,\"sbjRegDate\":null,\"reTypeExtension\":null,\"dcReSubType\":null,\"renRenID\":null,\"rnNum\":54020835,\"dcIrpSpread\":null,\"enumSPart\":null,\"enumSubPart\":null,\"enumEmph\":null,\"objectIdentifier\":null,\"reExtension\":null,\"addresses\":[{\"ID\":39785395,\"rreRreID\":54020835,\"rrpRrpID\":null,\"atuAtuID\":null,\"house\":null,\"building\":null,\"objectNum\":null,\"rrpRnNum\":null,\"houseHash1\":null,\"houseHash2\":null,\"roomHash1\":null,\"additional\":null,\"dcObjectNumType\":null,\"room\":null,\"isNotFull\":null,\"dcReOwnerKind\":\"1\",\"simpleAddress\":null,\"isSimpleAddress\":\"0\",\"objectNumHash1\":null,\"objectNumHash2\":null,\"roomHash2\":null,\"dcHouseType\":null,\"dcRoomType\":null,\"groupNum\":1,\"buildingHash2\":null,\"dcBuildingType\":null,\"buildingHash1\":null,\"addressInfo\":\"\"}],\"cadNums\":[{\"ID\":36556042,\"rrpRrpID\":null,\"rreRreID\":54020835,\"enum\":\"8000000000:85:289:0006\",\"rrpRnNum\":null,\"cadNumHash\":\"8000000000852890006\"}],\"reType\":\"земельна ділянка\",\"reTypeOnm\":\"земельна ділянка\"}],\"paymentDocuments\":[{\"ID\":102820242,\"rpdRpdID\":null,\"reqReqID\":60885663,\"enum\":\"22\",\"pdType\":null,\"dcPayType\":\"5\",\"summ\":100,\"dcChangeType\":\"2\",\"dcPdReasonType\":null,\"rnNum\":102820242,\"additional\":null,\"reqRnNum\":51230684,\"orgName\":\"банк\",\"dcPdKind\":\"1\",\"rpdDate\":\"2022-11-23T00:00:00Z\",\"pdReasonTypeExtension\":null,\"reportResultID\":null,\"receiptNum\":null,\"payType\":\"Адміністративний збір за реєстраційні дії\"}],\"causeDocuments\":[{\"ID\":338459458,\"cdCdID\":null,\"dcCdSort\":\"1\",\"dcCdType\":\"108\",\"publisher\":\"Державний земельний кадастр\",\"enum\":\"55241333\",\"dcCdReasonType\":null,\"attrReqRnNum\":null,\"rceRnNum\":null,\"baseCdID\":null,\"ropRopID\":null,\"lmLmID\":null,\"mgMgID\":null,\"irpIrpID\":null,\"dcChangeType\":\"2\",\"bnRnNum\":null,\"baseRnNum\":null,\"prRnNum\":null,\"docTypeUser\":null,\"additional\":null,\"reqReqID\":60885663,\"rnNum\":338459458,\"lmRnNum\":null,\"dcCdKind\":\"12\",\"dcEntityClass\":\"1\",\"cdTypeExtension\":null,\"cdReasonTypeExtension\":null,\"rceRceID\":null,\"attrReqID\":null,\"reqRnNum\":51230684,\"irpRnNum\":null,\"bnBnID\":null,\"docDate\":\"2022-11-23T00:00:00Z\",\"expirationDate\":null,\"opOpID\":null,\"reReID\":null,\"mgRnNum\":null,\"breRnNum\":null,\"oedOedID\":null,\"reRnNum\":null,\"prPrID\":null,\"breBreID\":null,\"documentID\":355127189,\"cdType\":\"відомості з ДЗК\",\"pagesCount\":1,\"sortOrder\":355127189,\"uploadedPages\":1,\"countPages\":null,\"deliveryDate\":null,\"rercRercID\":null,\"pageFiles\":[{\"ID\":228952387,\"documentID\":355127189,\"pageNumber\":1,\"cdID\":338459458,\"empEmpID\":25213,\"dcCdType\":\"108\",\"addedDate\":\"2022-11-23T23:22:37Z\",\"signature\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"16419913.p7s\\\",\\\"origName\\\":\\\"16419913.p7s\\\",\\\"relPath\\\":\\\"202211/23\\\",\\\"ct\\\":\\\"application/pkcs7-signature\\\",\\\"size\\\":3782,\\\"md5\\\":\\\"6796e4a412fb99a266b0eb1212c12a1e\\\",\\\"revision\\\":1}\",\"generatedDocument\":\"{\\\"v\\\":1,\\\"store\\\":\\\"causeDocumentFiles\\\",\\\"fName\\\":\\\"no-file-name.bin\\\",\\\"origName\\\":\\\"no-file-name.bin\\\",\\\"relPath\\\":\\\"202211/23\\\",\\\"ct\\\":\\\"application/octet-stream\\\",\\\"size\\\":54327,\\\"md5\\\":\\\"f2a2cd35936b5c29dcba9a24f7363d6b\\\",\\\"revision\\\":1}\"}],\"isDabiEcd\":true}],\"dzk\":[{\"ID\":18719019,\"areaUnit\":\"га\",\"dcAreaUnit\":null,\"techDoc\":\"Проект землеустрою щодо відведення земельних ділянок, 26.05.2008\",\"ownershipForm\":\"Комунальна власність\",\"cadNum\":\"8000000000:85:289:0006\",\"purpose\":\"Для розміщення та експлуатації основних, підсобних і допоміжних будівель та споруд підприємств переробної, машинобудівної та іншої промисловості\",\"regDate\":\"2008-05-30T00:00:00Z\",\"reqReqID\":60885663,\"state\":\"зареєстровано\",\"orgName\":\"Головне управління земельних ресурсів виконавчого органу Київради (Київської міської державної адміністрації)\",\"area\":\"1.4415\",\"purposeCode\":\"11.02\",\"cdCdID\":338459458,\"ddpfDdpfID\":228952387,\"address\":[{\"ID\":18565699,\"building\":\"40\",\"block\":null,\"rdzkRdzkID\":18719019,\"streetName\":\"вул. Фрунзе\",\"region\":\"м. Київ\",\"settlement\":null,\"streetType\":null,\"additionalInfoBlock\":null,\"district\":\"м. Київ\"}],\"subject\":[{\"ID\":22044813,\"sbjCode\":\"22883141\",\"name\":null,\"docReasonCompany\":null,\"docRightNumber\":null,\"rdzkRdzkID\":18719019,\"type\":\"юридична особа\",\"docRightType\":null,\"part\":\"1/1\",\"docRightDate\":null,\"passport\":null,\"docReasonNumber\":null,\"legalMode\":\"Право власності\",\"docReasonType\":null,\"servitudeMode\":null,\"irpDate\":null,\"irpTerm\":null,\"irpArea\":null,\"docRightCompany\":null,\"docReasonDate\":null}]}],\"holder\":{\"empEmpID\":25213,\"objObjID\":22061,\"objObjnID\":4367,\"atuAtuID\":10,\"objectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"objectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"atuName\":\"Київська обл.\",\"notaryDepName\":\"Фастівський районний нотаріальний округ\"},\"reqState\":\"зареєстровано\",\"lastOpID\":168554009,\"registrarEmpID\":25213,\"registrarEmployeeName\":\"Панікар Валентина Миколаївна\",\"registrarAtuID\":10,\"registrarAtuName\":\"Київська обл.\",\"registrarObjID\":22061,\"registrarObjectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"registrarObjnID\":4367,\"registrarObjectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"registrarInfo\":\"<b>Панікар Валентина Миколаївна</b>, Києво-Святошинська районна державна нотаріальна контора, Київська обл.\",\"registrarInfoExists\":true,\"reqType\":\"заява про державну реєстрацію прав\",\"reqSort\":\"паперова\",\"docGiveType\":\"особисто\",\"extReceiveType\":\"у паперовому вигляді\",\"holderEmpID\":25213,\"holderEmployeeName\":\"Панікар Валентина Миколаївна\",\"holderObjectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"holderObjectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"holderAtuName\":\"Київська обл.\",\"operations\":[{\"ID\":168554009,\"dcOpType\":\"1\",\"opDate\":\"2022-11-23T23:22:37Z\",\"empEmpID\":25213,\"objObjID\":22061,\"objObjnID\":4367,\"atuAtuID\":10,\"dcOpReasonType\":null,\"opReasonTypeExtension\":null,\"opReason\":null,\"additional\":null,\"registrarEmpID\":25213,\"registrarObjID\":22061,\"registrarObjnID\":4367,\"registrarAtuID\":10,\"dcEntityClass\":\"1\",\"isLastOp\":\"1\",\"dsRnNum\":null,\"toHID\":130781310,\"reasonDsRnNum\":null,\"cancelRopID\":null,\"objectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"registrarObjectName\":\"Києво-Святошинська районна державна нотаріальна контора\",\"objectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"registrarObjectNameHist\":\"Києво-Святошинська районна державна нотаріальна контора\",\"opType\":\"Реєстрація заяви\",\"employeeName\":\"Панікар Валентина Миколаївна\",\"registrarEmployeeName\":\"Панікар Валентина Миколаївна\",\"atuName\":\"Київська обл.\",\"registrarAtuName\":\"Київська обл.\",\"entityClass\":\"заява\"}],\"decisionsAndDocs\":[],\"colorClass\":\"#ffd000\",\"isExistsPrintDoc\":0}",
                "repReportResultID": None,
                "isAllowAnnullate": False,
                "privPrefix": "NOTAR",
                "operation": "RequestPdf"
            }
        ]

        response_generate_pdf_st_card = self.client.post("/ubql", name=self.class_name + " (DRRP)stvorennya DF zayavi",
                                                         headers=self.headers,
                                                         json=data_generate_pdf_st_card)
        report_result_id_generate_st_pdf = response_generate_pdf_st_card.json()[0].get('reportResultID')

        data_get_doc_st_pdf = {
            "entity": "rep_reportResult",
            "attribute": "generatedDocument",
            "ID": report_result_id_generate_st_pdf,
            "store": "reportsLU",
            "origName": '{report_result_id}{pdf}'.format(report_result_id=str(report_result_id_generate_st_pdf),
                                                         pdf='.pdf'),
            "filename": 'rep_reportResult{report_result_id}generatedDocument'.format(
                report_result_id=str(report_result_id_generate_st_pdf)),
            "_rc": 1
        }
        # self.client.get("/getDocument", name=self.class_name + " (DRRP)vidkrittya DF zayavi", headers=self.headers,
        #                 params=data_get_doc_st_pdf)

        # Відкриття вкладки Передача прав на обробку заяв та запитів
        self.client.post("/ubql", name=self.class_name + " (DRRP)Vidkrittya peredacha prav na obrobotru",
                         headers=self.headers,
                         json=erc_objects_names_atu)

        # Передача прав на обробку заяв та запитів
        data = [
            {
                "entity": "rrpUb_requestCard",
                "method": "transferRights",
                "instance": "{\"requests\":[" + str(
                    rn_num) + "],\"opReason\":\"Автотест\",\"atuAtuID\":2,\"objectID\":20793}"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)Peredacha prav na obrobotru",
                         headers=self.headers,
                         json=data)

    @task
    def queue_el_st(self):
        data = [
            {
                "entity": "rrpUb_pkgRequest",
                "method": "select",
                "privPrefix": "NOTAR",
                "fieldList": [
                    "ID",
                    "miCreateDate",
                    "reqType",
                    "subjects",
                    "dcTermReview",
                    "termReviewDate",
                    "mi_modifyDate"
                ],
                "options": {
                    "limit": 30,
                    "start": 0
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)Vidkrittya chergi zayav podanish elect formi",
                         headers=self.headers,
                         json=data)

    @task
    def search_st_preregistration(self):
        # Відкриття вкладки Пошук заяв на попередню реєстрацію
        self.client.post("/ubql", name=self.class_name + " (DRRP)Vidkrittya poshuk zayav prev reestratsii",
                         headers=self.headers,
                         json=erc_objects_names_atu)

        # Пошук заяв на попередню реєстрацію
        data = [
            {
                "entity": "rrpUb_requestCard",
                "method": "searchRequestPreRegistration",
                "searchParams": {
                    "reqStartDate": get_date_strftime("%Y-%m-%dT%H-2:%M:%S.000Z", 10),
                    "reqFinishDate": get_now_strftime("%Y-%m-%dT%H-2:%M:%S.000Z"),
                    "holderObjId": 22061,
                    "dcHolderType": 914,
                    "holderAtuId": 10,
                    "privCode": "NOTAR_PREV_REQ_OPERATIONS_SEARCH"
                }
            }
        ]
        self.client.post("/ubql",
                         name=self.class_name + " (DRRP)poshuk zayav prev reestratsii(searchRequestPreRegistration)",
                         headers=self.headers,
                         json=data)

    # -- Сутності які викликаються при авторизації
    @task()
    def auth_ubs_settings(self):
        data = [
            {
                "entity": "ubs_settings",
                "method": "select",
                "fieldList": [
                    "ID",
                    "settingKey",
                    "name",
                    "description",
                    "type",
                    "settingValue",
                    "defaultValue"
                ],
                "version": "166"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)ubs_settings", headers=self.headers, json=data)

    def auth_ubm_form_ubm_enum(self):
        data = [
            {
                "entity": "ubm_enum",
                "method": "select",
                "fieldList": [
                    "eGroup",
                    "code",
                    "name",
                    "shortName",
                    "sortOrder",
                    "ID",
                    "mi_modifyDate"
                ],
                "version": "251207"
            },
            {
                "entity": "ubm_form",
                "method": "select",
                "fieldList": [
                    "ID",
                    "code",
                    "description",
                    "caption",
                    "formType",
                    "formDef",
                    "formCode",
                    "entity",
                    "model",
                    "isDefault"
                ],
                "version": 803741496
            },
            {
                "entity": "ubm_enum",
                "method": "select",
                "fieldList": [
                    "ID",
                    "eGroup",
                    "code",
                    "name",
                    "shortName",
                    "sortOrder",
                    "mi_modifyDate"
                ],
                "version": "251207"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)ubm_form ubm_enum", headers=self.headers, json=data)

    def auth_ubm_navshortcut(self):
        data = [
            {
                "entity": "ubm_navshortcut",
                "method": "select",
                "fieldList": [
                    "ID",
                    "desktopID",
                    "parentID",
                    "code",
                    "isFolder",
                    "caption",
                    "inWindow",
                    "isCollapsed",
                    "displayOrder",
                    "iconCls",
                    "description",
                    "mi_modifyDate"
                ],
                "orderList": {
                    "0": {
                        "expression": "desktopID",
                        "order": "asc"
                    },
                    "1": {
                        "expression": "parentID",
                        "order": "asc"
                    },
                    "2": {
                        "expression": "displayOrder",
                        "order": "asc"
                    },
                    "3": {
                        "expression": "caption",
                        "order": "asc"
                    }
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)ubm_navshortcut", headers=self.headers, json=data)

    def auth_ubae_enum_adm(self):
        data = [
            {
                "entity": "ubaE_enum_adm",
                "method": "selectAllowedEnums"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)ubaE_enum_adm(selectAllowedEnums)",
                         headers=self.headers, json=data)

    def auth_rrpcore_dictreservedwords(self):
        data = [
            {
                "entity": "rrpCore_dictReservedWords",
                "method": "selectValidator"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)rrpCore_dictReservedWords(selectValidator)",
                         headers=self.headers, json=data)

    def auth_rstcore_dict(self):
        data = [
            {
                "entity": "rstCore_dict",
                "method": "selectForClient"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)rstCore_dict(selectForClient)",
                         headers=self.headers, json=data)

    def auth_rrpcore_dictenum(self):
        data = [
            {
                "entity": "rrpCore_dictEnum",
                "method": "select",
                "fieldList": [
                    "eGroup"
                ]
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)rrpCore_dictEnum", headers=self.headers, json=data)

    def auth_ubm_navshortcut_ubs_message(self):
        data = [
            {
                "entity": "ubm_navshortcut",
                "method": "select",
                "fieldList": [
                    "ID",
                    "desktopID",
                    "parentID",
                    "code",
                    "isFolder",
                    "caption",
                    "inWindow",
                    "isCollapsed",
                    "displayOrder",
                    "iconCls",
                    "description"
                ],
                "orderList": {
                    "0": {
                        "expression": "desktopID",
                        "order": "asc"
                    },
                    "1": {
                        "expression": "parentID",
                        "order": "asc"
                    },
                    "2": {
                        "expression": "displayOrder",
                        "order": "asc"
                    },
                    "3": {
                        "expression": "caption",
                        "order": "asc"
                    }
                }
            },
            {
                "entity": "ubs_message",
                "method": "getCached",
                "fieldList": [
                    "ID",
                    "messageBody",
                    "messageType",
                    "startDate",
                    "expireDate",
                    "recipients.acceptDate"
                ],
                "whereList": {
                    "c1": {
                        "expression": "[recipients.acceptDate]",
                        "condition": "isNull"
                    }
                },
                "orderList": {
                    "0": {
                        "expression": "startDate",
                        "order": "desc"
                    }
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)ubm_navshortcut, ubs_message", headers=self.headers,
                         json=data)

    def auth_ubm_enum_ubm_desktop(self):
        data = [
            {
                "entity": "ubm_enum",
                "method": "select",
                "fieldList": [
                    "ID",
                    "eGroup",
                    "code",
                    "name",
                    "sortOrder"
                ],
                "version": "251207"
            },
            {
                "entity": "ubm_desktop",
                "method": "select",
                "fieldList": [
                    "ID",
                    "caption",
                    "description",
                    "iconCls",
                    "isDefault",
                    "displayOrder"
                ],
                "version": "-1"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)ubm_enum, ubm_desktop", headers=self.headers,
                         json=data)

    def auth_rrp_core_dict_enum(self):
        self.client.post("/ubql", name=self.class_name + " (DRRP)rrpCore_dictEnum", headers=self.headers,
                         json=rrp_core_dict_enum)

    # Пошук сертифіката
    def search_certificate(self):
        data = [
            {
                "entity": "rrpDoc_certificateCard",
                "method": "search",
                "searchParams": {
                    "dcDocTypes": "\"6\"",
                    "series": "САК",
                    "num": "614544",
                    "isSimpleSearch": True
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)poshuk sertifikata(rrpDoc_certificateCard)",
                         headers=self.headers,
                         json=data)

    def erc_dict_countries(self):
        data = [
            {
                "entity": "erc_dict_countries",
                "method": "select",
                "fieldList": [
                    "ID",
                    "name",
                    "nameSearch"
                ],
                "whereList": {
                    "isActual": {
                        "expression": "[isActual]",
                        "condition": "equal",
                        "values": {
                            "isActual": 1
                        }
                    },
                    "byDefaultValue": {
                        "expression": "[ID]",
                        "condition": "equal",
                        "value": 225
                    }
                },
                "orderList": {
                    "byName": {
                        "expression": "[sortOrder]",
                        "order": "asc"
                    }
                }
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)erc_dict_countries)",
                         headers=self.headers,
                         json=data)

    def exchange_edr(self):
        data = [
            {
                "entity": "rrpExch_edr",
                "method": "getSubjects",
                "code": str(self.sbj_comp_code_list),
                "dcEntityType": "1"
            }
        ]
        self.client.post("/ubql", name=self.class_name + " (DRRP)obmin edr",
                         headers=self.headers,
                         json=data)
