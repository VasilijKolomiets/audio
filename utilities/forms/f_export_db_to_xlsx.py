# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 11:14:10 2022

@author: manager
"""
from pathlib import Path
import pandas as pd

from audio_models import connect_to_db, read
from utilities.utils import now_datetime_str
from utilities.common_excel_file_formatting import CommonExcelFileFormatting


def find_value_by_key(state_pars, key):
    for k, v_dict in state_pars.items():
        if key in v_dict:
            return str(v_dict[key])
    assert False, "wrong key for 'state_pars' dict!"


def f_export_db_to_xlsx(
        state_pars: dict = dict(),
        widget_dict: dict = dict(),
):
    """
    'items': {
        "db_name": 'items',
        "minsize": (500, 350),
        "title": "Дані продукції",
        "entries": {
            # '`id_items`'
            'delivery_contracts_id': {'text': 'код_поставки', 'type': int},
            'item_id_in_delivery':  {'text': 'item_id', 'type': int},
            'item_name': {'text': 'наименование_изделия', 'type': str},
            'item_weight': {'text': 'weight_1', 'type': float},
            'item_cost': {'text': 'value_1', 'type': float},
            'length': {'text': 'length:', 'type': int},
            'width': {'text': 'width', 'type': int},
            'height_x_100': {'text': 'height_x_100', 'type': float},
        },
        # value in dict have to match some key in 'state_params' dict, defined earlie here on top.
        "filter_on": {'delivery_contracts_id': "id_delivery_contract"},
    },

    """

    fields_list = sum(
        [list(widget_dict.get(key, {}).keys()) for key in ("labels", "entries", "radiobuttons")],
        []
    )
    fields_str = ", ".join(fields_list)
    table_name = widget_dict["db_name"]

    filters = ['TRUE', ]
    for key, key_v in widget_dict["app_filter_on"].items():
        filters.append("=".join([key, find_value_by_key(state_pars, key_v)]))
    filters_str = " AND ".join(filters)

    cursor = connect_to_db().cursor()
    try:
        fields = read(table_name,  fields_str,  conditions=filters_str,  cursor=cursor)
    finally:
        cursor.close()

    df_table = pd.DataFrame(
        fields,
        columns=fields_list,
    )

    file_name_parts = ["exported", table_name, now_datetime_str(), ".xlsx"]

    xlsx_file_name =  "_".join(file_name_parts)
    path_xlsx_file =  (Path(state_pars['dirs']['dir_xlsx_export']['dir_path']) / xlsx_file_name)

    formater_ =  (
        dict(
        sheet_name="Sheet01",
        colorize=[
            (
                'BISQUE',
                ('audiofile_name',  ),
            ),
        ],

        columns_num_format=[],
        widths={"A": 14,  'B:AZ': 80, },
        row_wraptext='1:1',
        columns_autofit=("A:A", ),
        freeze_panes="B2",
    ),
    )

    df_table.to_excel(path_xlsx_file.resolve(), sheet_name=formater_[0]['sheet_name'],  index=False )

    formater = CommonExcelFileFormatting(formater_)
    formater.excel_file_formatting({xlsx_file_name: path_xlsx_file})
