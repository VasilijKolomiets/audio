# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 09:37:41 2021

@author: manager

"""
# import pandas as pd
from pathlib import Path

from datetime import datetime as dt

# import fitz   # <-- PyMuPDF
# from PIL import Image, ImageDraw, ImageFont

path_ro_csv = Path(r'..\IN_DATA\zipCodes.csv')


def now_datetime_str() -> str:
    """Skip."""
    ddt = str(dt.now())  # '2022-02-03 14:04:47.060703'
    return ddt.replace(' ', "_").replace('.', "_").replace(":", "")


def my_str(object_: str):
    """"Replace the '!' ' '  '-' symbols."""
    return str(object_).replace('!', '_').replace('-', '_').replace(' ', '_')


if __name__ == '__main__':
    city_name, street_name = 'Біла Церква', 'вул. Олександрійська, 101'
