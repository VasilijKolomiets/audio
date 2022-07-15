"""Create on."""
# =============================================================================
# https://python-scripts.com/tkinter
# =============================================================================
from functools import partial

import tkinter as tk
from tkinter import ttk

import pandas as pd
import winsound


from settings import state_params, widgets_table
from utilities.forms.f_export_db_to_xlsx import f_export_db_to_xlsx
from utilities.forms.f_select_folder import f_pick_directory_to_state_dict
from recognize_audio import recognize_audio_in_folder

# """
# 'SystemAsterisk'
# 'SystemExclamation'
# 'SystemExit'
# 'SystemHand'
# 'SystemQuestion'

# import winsound
# freq = 2500 # Set frequency To 2500 Hertz
# dur = 1000 # Set duration To 1000 ms == 1 second
# winsound.Beep(freq, dur)

# freq = 100
# dur = 50

# # loop iterates 5 times i.e, 5 beeps will be produced.
# for i in range(0, 5):
#     winsound.Beep(freq, dur)
#     freq+= 100
#     dur+= 50
# """


def pick_directory_to_state_dict(state_params, dir_key):
    """Wrap f_pick_directory_to_state_dict()."""
    global audio_menu, var_lbl_statusbar

    f_pick_directory_to_state_dict(state_params, dir_key)

    if (dir_key == 'dir_audiofiles'):
        var_lbl_statusbar.set(F"Тека:: {state_params['dirs'][dir_key]['dir_path']}")
        audio_menu.entryconfigure("Розпізнати текст", state=tk.NORMAL)
        audio_menu.entryconfigure("Вибрати теку для експорту даних:", state=tk.NORMAL)


if __name__ == '__main__':

    root = tk.Tk()

    root.minsize(1000, 500)
    root.title('Аудіоконіертер')
    root.option_add("*Font", 'Verdana 13')

    mainframe = ttk.Frame(root, padding="2 5 2 2")
    # grid(column=0, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
    mainframe.pack(side=tk.BOTTOM, fill=tk.X)

    mainmenu = tk.Menu(mainframe)
    mainmenu.option_add("*Font", 'Verdana 13')
    root.config(menu=mainmenu)

    # import audio menu
    audio_menu = tk.Menu(mainmenu, tearoff=0)
    audio_menu.add_command(
        label="Вибрати теку aудіофайлів",
        # store to: state_params['dir_audiofiles']
        command=partial(pick_directory_to_state_dict, state_params, 'dir_audiofiles'),
    )
    audio_menu.add_command(
        label="Розпізнати текст",
        command=partial(recognize_audio_in_folder, state_params),
    )
    audio_menu.add_separator()
    audio_menu.add_command(
        label="Вибрати теку для експорту даних:",
        # store to: state_params['dir_xlsx_export']
        command=partial(pick_directory_to_state_dict, state_params, 'dir_xlsx_export'),
    )
    # export menu
    export_menu = tk.Menu(mainmenu, tearoff=0)
    export_menu.add_command(
        label="... в ексель",
        command=partial(f_export_db_to_xlsx, state_params, widgets_table['audiofiles'])
    )

    # exit menu
    exit_menu = tk.Menu(mainmenu, tearoff=0)
    exit_menu.add_command(label="Закрити програму", command=root.destroy)  # root.quit

    # main mrnu subscribing:
    mainmenu.add_cascade(label="Аудіофайли", menu=audio_menu)
    mainmenu.add_cascade(label="Експорт даних", menu=export_menu)
    mainmenu.add_cascade(label="Вихід", menu=exit_menu)

    audio_menu.entryconfigure("Розпізнати текст", state=tk.DISABLED)

    var_lbl_statusbar = tk.StringVar()
    var_lbl_statusbar.set("Тут будуть підказки…")

    lbl_statusbar = ttk.Label(mainframe,  # text="Тут будуть підказки…",
                              relief=tk.SUNKEN, anchor=tk.W,
                              textvariable=var_lbl_statusbar,
                              )
    state_params['statusbar'] = var_lbl_statusbar
    lbl_statusbar.pack(side=tk.BOTTOM, padx=1, pady=1, fill=tk.X)

    root.mainloop()
