"""[summary]
"""
# import sys
# from pathlib import Path


def from_server_connect():
    """
    Spyder Editor
    artlogis_new&password=t6zdxzfn
    artlogis_mysql_ukraine_com_ua.sql
    This is a temporary script file.

    +------------------------+
    | Tables_in_artlogis_new |
    +------------------------+
    | addresses              |
    | cities                 |
    | city_to_company        |
    | companies              |
    | deliveries_full_list   |
    | deliveries_short_list  |
    | orders_full_list       |
    | orders_short_list      |
    | users                  |
    | users_old              |
    +------------------------+

    """
    # Connecting from the server
    # connection = connector.connect(user="root",               # 'username',
    #                                host='localhost',
    #                                database="postman",         # 'database_name'
    #                                passwd="MySQL_password#5"
    #                                )
    # return connection


credentials = {
    'Meest': {
        'url':      r'https://api.meest.com/v3.0/openAPI',
        'username': r'art-pres_vkf_dnipro',
        'password': r'A^fFsnJR0OLG',
        'contract_id': "a3df71d8-5e17-11ea-80c6-000c29800ae7",
        'content_type': 'application/json',
    },
    'NovaPoshta': {
        'url':      r'https://api.meest.com/v3.0/openAPI',
        'username': r'art-pres_vkf_dnipro',
        'password': r'A^fFsnJR0OLG',
        'contract_id': "a3df71d8-5e17-11ea-80c6-000c29800ae7",
        'content_type': 'application/json',
    }
}


state_params = dict(
    client=dict(id_companies=None, name=None, fullname=None),
    delivery_contract=dict(id_delivery_contract=None, name=None),
    post_service=dict(id_postcervices=None, name=None),
    statusbar=None,
    selected_street=dict(id_street=None, name=None),
    dirs=dict(
        dir_audiofiles=dict(message='з аудіофайлами *.mp3', dir_path=None),
        dir_xlsx_export=dict(message='куди експортувати "xlsx" файл', dir_path="exported"),
    ),
)


tables_fields = {
    'audiofiles': [
        'id',
        'audiofile_name',
        'recognized_rus_text',
        'rus_text_translated_to_ukr',
    ],
}


widgets_table = {
    'audiofiles': {
        "db_name": 'audiofiles',
        "minsize": (600, 240),
        "title": "Розпізнані аудіофайли",

        # list of forms entries with their names:
        "entries": {
            'audiofile_name': {'text': 'Назва Компанії', 'type': str},
            'recognized_rus_text': {'text': 'Коротка назва латиницею', 'type': str},
            'rus_text_translated_to_ukr': {'text': 'Код ЄДРПОУ', 'type': int},
        },

        'app_filter_on': {},

        "radiobuttons": {},

    },

}
