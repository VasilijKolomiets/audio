# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 09:18:38 2021

@author: manager
"""
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo

from pathlib import Path

# import winsound
# from settings import state_params


def select_directory(in_title_text):
    foldername = askdirectory(title=F'Виберіть теку {in_title_text}:',  initialdir='.')
    showinfo(title='Вибрано теку:',  message=foldername)
    return foldername


def f_pick_directory_to_state_dict(state_pars: dict, dir_key):
    # winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    # get the file name
    directory_with_audiofiles_name = select_directory(state_pars['dirs'][dir_key]['message'])
    state_pars['dirs'][dir_key]['dir_path'] = Path(directory_with_audiofiles_name)
    print(F'=======================>{directory_with_audiofiles_name =}')

if __name__ == "__main__":
    ...
