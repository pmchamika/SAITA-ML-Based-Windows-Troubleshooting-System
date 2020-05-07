import datetime
from Data.Veriables import log_file, log_enable_all, log_enable_error, log_enable_warning

log_types = ["Error", "Warning", "Info"]


def get_curent_date_and_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def add_log(log_type, file_name, data):
    if log_enable_all:
        f = open(log_file, "a")
        f.write(get_curent_date_and_time() + " : " + file_name + "\n")
        f.write("\t" + log_type + " : " + data + "\n")
        f.close()
    elif log_enable_warning and (log_type == log_types[0] or log_type == log_types[1]):
        f = open(log_file, "a")
        f.write(get_curent_date_and_time() + " : " + file_name + "\n")
        f.write("\t" + log_type + " : " + data + "\n")
        f.close()
    elif log_enable_error and log_type == log_types[0]:
        f = open(log_file, "a")
        f.write(get_curent_date_and_time() + " : " + file_name + "\n")
        f.write("\t" + log_type + " : " + data + "\n")
        f.close()
