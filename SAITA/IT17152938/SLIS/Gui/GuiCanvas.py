import urllib
from tkinter import *
from tkinter.ttk import Combobox
from urllib.error import *
from tkinter.messagebox import *
from win32api import GetMonitorInfo, MonitorFromPoint
from PIL import ImageTk, Image
from Data.Veriables import *
from Data.Log import *
from Util.MainController import MainController
import math
from urllib.request import urlopen
from Util.Software import Software

# get monitor working aria size
monitor_fo = GetMonitorInfo(MonitorFromPoint((0, 0)))
add_log(log_types[2], "GuiCanvas.py", "Monitor info : " + str(monitor_fo))
work_area = monitor_fo.get("Work")
acc_ra = work_area[3] / work_area[2]
add_log(log_types[2], "GuiCanvas.py", "set acc_ra: " + str(acc_ra))

# search box
search_box = None
# search button
search_but = None

# body
body_window = None
body_window_canves = None

# img array
soft_img_array = None

# add_button_array
add_button_array = None

# select_box_array
select_box_array = None
select_box_value_array = None

# install list = []
install_list = []


def create_full_show_window(win_root):
    full_show_window = Frame(win_root, bg=full_window_color, highlightthickness=0)
    head_show_window = create_head_show_window(full_show_window)
    body_show_window = create_body_show_window(full_show_window)
    head_show_window.pack(fill=X)
    body_show_window.pack(expand=1, fill=BOTH)
    return full_show_window


def create_head_show_window(full_window):
    global search_box, search_but
    head_window = Frame(full_window, bg=head_window_color, highlightthickness=0)
    search_box = Entry(head_window,
                       bg=main_search_color_bg,
                       fg=main_search_color_txt,
                       font="bold",
                       width=round(main_search_width * acc_ra)
                       )
    search_box.pack(
        side=LEFT,
        padx=pad_val * acc_ra,
        pady=pad_val * acc_ra,
        ipadx=pad_val * acc_ra,
        ipady=pad_val * acc_ra

    )

    search_but = Button(head_window,
                        text=main_search_but_txt,
                        bg=main_search_but_bg,
                        activebackground=main_search_but_acc,
                        bd=2,
                        font="bold",
                        fg=main_search_but_txt_color,
                        activeforeground=main_search_but_txt_color,
                        highlightthickness=0,
                        )

    search_but.pack(
        side=LEFT,
        padx=pad_val * acc_ra,
        pady=pad_val * acc_ra,
        ipadx=main_search_but_ipadx * acc_ra,
        ipady=main_search_but_ipady * acc_ra,
    )

    # bind search key to event
    search_but.bind("<Button-1>", search_soft)
    search_but.bind("<Enter>", search_button_hover_in)
    search_but.bind("<Leave>", search_button_hover_out)
    search_box.bind("<Return>", search_soft)
    search_box.bind("<KeyRelease>", search_key_enter)

    return head_window


def create_body_show_window(full_window):
    global body_window, body_window_canves
    main_body_window = Frame(full_window, bg=body_window_color, highlightthickness=0, padx=pad_val * acc_ra,
                             pady=pad_val * acc_ra)
    body_window_canves = Canvas(main_body_window, bg=body_window_color, highlightthickness=0)
    body_window = Frame(body_window_canves, bg=body_window_color)
    body_scrollbar = Scrollbar(main_body_window, orient="vertical", command=body_window_canves.yview)
    body_window_canves.configure(yscrollcommand=body_scrollbar.set)
    body_scrollbar.pack(side="right", fill="y")
    body_window_canves.pack(expand=1, fill=BOTH)
    body_window_canves.create_window((0, 0), window=body_window, anchor='nw')
    body_window.bind("<Configure>", scroll_all)
    main_con = MainController()
    soft_list = main_con.get_soft_list_full()
    create_body_data(soft_list)
    return main_body_window


def search_key_enter(event):
    global search_box
    if search_box.get() == "":
        add_log(log_types[2], "GuiCanvas.py", "search_key_enter : " + str(event) + "  Data : Empty search bar")
        main_con = MainController()
        soft_list = main_con.get_soft_list_full()
        create_body_data(soft_list)


def search_soft(event):
    global search_box
    add_log(log_types[2], "GuiCanvas.py", "search_soft : " + str(event) + "  Data : " + search_box.get())
    main_con = MainController()
    soft_list = main_con.get_soft_list_search(search_box.get())
    create_body_data(soft_list)


def search_button_hover_in(event):
    global search_but
    add_log(log_types[2], "GuiCanvas.py", "search_button_hover_in : " + str(event))
    search_but['bg'] = main_search_but_hover


def search_button_hover_out(event):
    global search_but
    add_log(log_types[2], "GuiCanvas.py", "search_button_hover_out : " + str(event))
    search_but['bg'] = main_search_but_bg


def scroll_all(event):
    global body_window_canves
    add_log(log_types[2], "GuiCanvas.py", "scroll_all : " + str(event))
    body_window_canves.configure(scrollregion=body_window_canves.bbox("all"))


def create_body_data(soft_list):
    global body_window, work_area, acc_ra, soft_img_array, add_button_array, select_box_array, select_box_value_array
    # soft_img_array = None
    soft_img_array = []
    # add_button_array = None
    add_button_array = []
    # select_box_array = None
    select_box_array = []
    select_box_value_array = []
    wid = round((work_area[2] - (round(pad_val * acc_ra) * coll_count)) / coll_count)
    soft_title_f_size = round((soft_title_f_size_dev / coll_count) / acc_ra)
    soft_ver_f_size = round((soft_ver_f_size_dev / coll_count) / acc_ra)
    add_log(log_types[2], "GuiCanvas.py", "create_body_data : " + str(soft_list))
    ch = 0
    x_range = math.ceil(len(soft_list) / coll_count)
    # x_range = 50
    # clear body window
    for widget in body_window.winfo_children():
        widget.destroy()

    for x in range(x_range):
        row_frame = Frame(body_window, bg=body_window_color, highlightthickness=0)
        for y in range(coll_count):
            if ch == len(soft_list):
                break
            else:
                singal_frame = Frame(row_frame, bg=body_window_color, highlightthickness=0, width=wid, height=wid,
                                     padx=pad_val * acc_ra, pady=pad_val * acc_ra)
                singal_frame_in = Frame(singal_frame, bg=cell_bg, width=wid, height=wid,
                                        relief='raised',
                                        bd=0)
                singal_frame.pack(side=LEFT, )
                singal_frame.pack_propagate(0)
                singal_frame_in.pack(side=LEFT, expand=True)
                singal_frame_in.pack_propagate(0)

                # soft image
                url_img = img_location + soft_list[ch]['img']
                soft_img = None
                try:
                    soft_img = Image.open(urlopen(url_img))
                except HTTPError as err:
                    add_log(log_types[1], "GuiCanvas.py", "Image not found in : " + url_img + " error : " + str(err))
                    soft_img = Image.open(not_found_img)
                except URLError as err:
                    add_log(log_types[0], "GuiCanvas.py", "Cant connect resources server : " + str(err))
                    soft_img = Image.open(not_found_img)

                soft_img_w, soft_img_h = soft_img.size
                soft_img_w /= (coll_count * soft_img_dev)
                soft_img_h /= (coll_count * soft_img_dev)
                soft_img = soft_img.resize((round(soft_img_w), round(soft_img_h)))
                soft_img_get = ImageTk.PhotoImage(soft_img)
                soft_img_array.append(soft_img_get)
                soft_img_labal = Label(singal_frame_in, image=soft_img_array[ch], bg=cell_bg, )
                soft_img_labal.pack(expand=True, fill='x')
                # soft name
                soft_topic = Label(singal_frame_in, text=soft_list[ch]['name'], bg=cell_bg, fg=cell_topic_txt_color,
                                   font="bold", pady=0)
                soft_topic.config(font=("arial", soft_title_f_size))
                soft_topic.pack(expand=True, fill='x')

                # -------------------version frame---------------------
                ver_frame = Frame(singal_frame_in, bg=cell_bg,
                                  relief='raised',
                                  bd=0)
                ver_frame.pack(expand=True, fill=X)
                # version Labal
                soft_ver_la = Label(ver_frame, text="Version :", bg=cell_bg, fg=cell_topic_txt_color,
                                    font="bold", )
                soft_ver_la.config(font=("arial", soft_ver_f_size))
                soft_ver_la.pack(expand=True, side=LEFT)

                # version Box
                soft_ver_box = create_combobox(ver_frame, soft_list[ch])
                select_box_array.append(soft_ver_box)
                select_box_array[ch].config(font=("arial", round(soft_ver_f_size * 0.7)))
                select_box_array[ch].pack(expand=True, side=LEFT)
                select_box_array[ch].bind("<<ComboboxSelected>>",
                                          lambda eff, array_id_pass=ch, get_soft_name=soft_list[ch]['name']:
                                          select_box_change(eff, array_id=array_id_pass, soft_name=get_soft_name))

                # ----------------------------------------

                # add button

                soft_add_butt = Button(singal_frame_in,
                                       text='+',
                                       bg=soft_add_butt_bg,
                                       activebackground=soft_add_butt_acc,
                                       bd=0,
                                       font="bold",
                                       fg=soft_add_butt_txt,
                                       activeforeground=soft_add_butt_txt,
                                       highlightthickness=0
                                       )

                soft_add_butt.config(font=("arial", round(soft_title_f_size * 1.5)))
                soft_add_butt.pack(expand=True, fill=X)
                add_button_array.append(soft_add_butt)
                add_button_array[ch].bind("<Button-1>", lambda eff, soft_id_get=soft_list[ch]['id'], array_id_pass=ch:
                add_click(eff, soft_id=soft_id_get, array_id=array_id_pass))
                add_button_array[ch].bind("<Enter>", lambda eff, array_id_pass=ch:
                add_btn_on_hovering(eff, add_id=array_id_pass))
                add_button_array[ch].bind("<Leave>", lambda eff, array_id_pass=ch:
                add_but_return_to_normal_state(eff, add_id=array_id_pass))
                ch += 1
        row_frame.pack(fill=X)


def select_box_change(event, array_id, soft_name):
    global select_box_array
    select_text_point = select_box_array[array_id].current()
    if select_text_point != -1:
        select_text = select_box_array[array_id].get()
        select_text_split = select_text.split('installed')
        if len(select_text_split) > 1:
            select_box_array[array_id].set('')
            showwarning("Warning", soft_name + " " + select_text_split[0] + "already installed")


def add_click(event, soft_id, array_id):
    global select_box_array, select_box_value_array, install_list, add_button_array
    select_text_point = select_box_array[array_id].current()
    if select_text_point != -1:
        add_log(log_types[2], "GuiCanvas.py",
                "add_click  soft_id : " + str(soft_id) + " event : " + str(event) + " array_id : " + str(array_id))
        ver_id_array = select_box_value_array[array_id]
        if len(ver_id_array) > 0:
            ver_id = ver_id_array[select_text_point]
            cr_array = {'soft_id': soft_id, 'ver_id': ver_id, 'select_text_point': select_text_point}
            if add_button_array[array_id]['text'] == '+':
                add_button_array[array_id]['text'] = '-'
                install_list.append(cr_array)
            else:
                add_button_array[array_id]['text'] = '+'
                install_list.remove(cr_array)
            print(install_list)
    else:
        showinfo("Warning", "Select Software version")


def create_combobox(frame, object):
    global select_box_value_array
    ver_array = []
    ver_id_array = []
    for ver in Software().get_all_version(object['id']):
        txt = "Ver : " + str(ver['v_no'])
        # if ver['v_name'] != "":
        #     txt += " , Name: " + ver['v_name']

        if 'installed_ver' in object:
            for inst_ver in object['installed_ver']:
                inst_split = inst_ver.split('.')
                inst_ok = None
                v_no_split = str(ver['v_no']).split('.')
                v_no_ok = None
                if len(inst_split) > 1:
                    inst_ok = inst_split[0] + "." + inst_split[1]
                else:
                    inst_ok = inst_split[0] + ".0"

                if len(v_no_split) > 1:
                    v_no_ok = v_no_split[0] + "." + v_no_split[1]
                else:
                    v_no_ok = v_no_split[0] + ".0"

                if inst_ok == v_no_ok:
                    txt += "  installed"
        ver_array.append(txt)
        ver_id_array.append(ver['id'])

    select_box_value_array.append(ver_id_array)
    com_box = Combobox(frame, values=ver_array, font="bold", state="readonly")
    return com_box


def add_btn_on_hovering(event, add_id):
    global add_button_array
    add_log(log_types[2], "GuiMain.py", "add_btn_on_hovering : " + str(event))
    add_button_array[add_id]['bg'] = soft_add_butt_hover


def add_but_return_to_normal_state(event, add_id):
    global add_button_array
    add_log(log_types[2], "GuiMain.py", "add_but_return_to_normal_state : " + str(event))
    add_button_array[add_id]['bg'] = soft_add_butt_bg
