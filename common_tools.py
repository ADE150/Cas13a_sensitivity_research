import pymol
import selenium
import requests
import re
import pickle
import os
from time import sleep
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import seaborn as sns
from matplotlib import font_manager as fm
from selenium import webdriver
from openpyxl.utils.dataframe import dataframe_to_rows
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl

# 根目录，需要根据项目所在的文件夹进行调整
# 不能用os.getcwd()方法，否则子文件夹无法访问到其他文件夹，或者只能通过「../」访问（麻烦）
root_dir = r"C:\Users\29701\Desktop\毕业设计\04 毕设-结果-结果分析\Python与PyMOL批量处理"

# 输出日志，注释掉里面的print可以一次性关闭所有输出
def print_stack_trace(any):
    print(any)


# 输出类型，注释掉里面的print可以一次性关闭所有输出
def printType(any):
    print(type(any))


# 输出提醒
def remind(any):
    print(any)


def remind_start(any):
    remind(f"————  {any} ————\n")


def remind_detail(A, B=""):
    remind(f"{A}：{B}" if len(B) != 0 else f"- {A}")


def remind_end(any):
    remind(f"————————  {any} 结束\n")


# 连接目录
def con_frag(*paths):
    return os.path.join(*paths)


# 得到文件名
def get_filename(dir):
    return os.path.basename(dir)


# 得到不含扩展的文件名
def get_filename_without_suffix(dir):
    mid = os.path.splitext(get_filename(dir))
    return mid[0] if len(mid) != 0 else dir


# 判断当前目录是否存在这个文件
def exist_file(file_name, directory=root_dir):
    file_dir = con_frag(directory, file_name)
    return os.path.exists(file_dir)


def find_first_str(text, pattern):
    mid = re.findall(pattern, text, re.I | re.M)
    return mid[0] if len(mid) != 0 else text


def get_PDB_filenames(dir, is_sort=1):
    PDB_filenames = [f for f in os.listdir(dir) if f.endswith(".pdb")]
    if is_sort == 1:
        PDB_filenames.sort(key=lambda x: (x[:3], int(find_first_str(x, r"_(.+?)\.pdb"))))
    else:
        print_stack_trace(is_sort)
    return PDB_filenames


def get_object_names(dir, is_sort=1):
    object_names = [os.path.splitext(f)[0] for f in get_PDB_filenames(dir, is_sort)]
    return object_names


def get_PDB_paths(dir, is_sort=1):
    PDB_paths = [con_frag(dir, f) for f in get_PDB_filenames(dir, is_sort)]
    return PDB_paths


# 选择特定部分并从主体中永久删除
def select_and_remove(selection, sel_name="temp", limit=None):
    pymol_cmd = pymol.cmd
    pymol_cmd.select(sel_name, selection)
    pymol_cmd.remove(sel_name)
    pymol_cmd.delete(sel_name)


# 删除溶剂分子和非正常残基
def remove_solvent(object=None):
    solvent_text = f"solvent and object {object}" if object != None else "solvent"
    abnormal_resn_text = f"resn 0+POT+CLA and object {object}" if object != None else "resn 0+POT+CLA"
    select_and_remove(solvent_text, "solvent_all")
    select_and_remove(abnormal_resn_text, "other_solvent")


# 保存Pymol文件
def pymol_cmd_save(path, selection="(all)"):
    pymol_cmd.save(path, selection)
    filename = os.path.basename(path)
    if (exist_file(filename)):
        print_stack_trace(f"正在保存{filename}，该文件将覆盖原有的同名文件！")


# 打开浏览器
def open_edge():
    global web_edge_driver
    web_edge_driver = webdriver.Edge()


def write_to_excel(a_path, a_list, index=False):
    df = pd.DataFrame(a_list)
    df.to_excel(a_path, index=index)


def remove_selection(selection="(all)"):
    pymol_cmd.remove(selection)


# TODO 指定字体路径，但目前还找不到显示“Å”的方式
def set_plot_font():
    # font_path = r'C:\Windows\Fonts\苹方 中.ttf'  # 替换为实际字体文件路径
    font_path = r'C:\Users\29701\AppData\Local\Microsoft\Windows\Fonts\PingFang-Medium.ttf'  # 替换为实际字体文件路径
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.sans-serif'] = [font_prop.get_name()]  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    # 简单设置中文字体的方式
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    # plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

def get_cwd_excels():
    return [f for f in os.listdir(os.getcwd()) if f.endswith(".xlsx")]

def close_all_fig(figs):
    for fi in figs:
        plt.close(fi)

def load_no_solvent(path,obj):
    pymol_cmd.load(path,obj)
    remove_solvent(obj)

# 通过workbook写入多个表格，args要用元组：（表格名称，数据）
# 数据格式为[{a:1,b:Str1},{a:2,b:Str2}]或{a:[1,2],b:[Str1,Str2]}
def write_multi_sheet_to_excel_1(dir,*args):
    workbook=openpyxl.Workbook()
    workbook.remove(workbook.active)
    for sheet_name,data in args:
        df=pd.DataFrame(data)
        sheet=workbook.create_sheet(title=sheet_name)
        for r in dataframe_to_rows(df, index=False, header=True):
            sheet.append(r)
    workbook.save(dir)

# 通过pandas写入多个表格，args要用元组：（表格名称，数据）
# 数据格式为[{a:1,b:Str1},{a:2,b:Str2}]或{a:[1,2],b:[Str1,Str2]}
def write_multi_sheet_to_excel_2(dir,*args):
    with pd.ExcelWriter(dir) as writer:
        for sheet_name,data in args:
            df=pd.DataFrame(data)
            df.to_excel(writer,sheet_name=sheet_name,index=False)


class PathManager:
    def __init__(self, base_path):
        self.base_path = base_path

    def get_path(self, dotted_path):
        """
        Convert a dot-separated path to an actual file system path.

        :param dotted_path: 使用“.”分开路径名 (e.g., "folder.subfolder.file")
        :return: 返回完整的路径
        """
        return os.path.join(self.base_path, *dotted_path.split('.'))


pymol_cmd = pymol.cmd

web_edge_driver = None


# 根目录的文件夹名称
install_pymol_dir = "00_install_pymol"
get_Cas13a_designer_dir = "01_get_Cas13a_designer"
molecular_dynamics_simulation_dir = "02_molecular_dynamics_simulation"
SASA_analysis_dir = "03_SASA_analysis"
get_dis_bases_and_nearby_dir = "04_get_dis_bases_and_nearby"
# 子文件夹名称
catalytic_core_PDB_files_dir = "catalytic_core_PDB_files"
catalytic_core_PDB_files_dir_with_solvent = "_catalytic_core_PDB_files_with_solvent"

# 获取40帧PDB文件所在目录
origin_PDB_path = con_frag(root_dir,molecular_dynamics_simulation_dir)
# 导入40帧PDB文件的对象的文件路径
all_origin_object_path =con_frag(root_dir,molecular_dynamics_simulation_dir,"all_origin_object.pse")

# 可能被用到的文件
# distance_and_angle_dir= "distance_and_angle"
# contact_analysis_dir="contact_analysis"
# nearby_resis_dir="nearby_resis"

# # 放处理后的Pymol文件
# intermediate_products_dir= r"C:\Users\29701\Desktop\毕业设计\04 毕设-结果-结果分析\Python与PyMOL批量处理\intermediate_products"
# # 放计算结果和图表
# output_dir= r"C:\Users\29701\Desktop\毕业设计\04 毕设-结果-结果分析\Python与PyMOL批量处理\05_已得到且已处理的数据文件"

all_PDB_paths = get_PDB_paths(origin_PDB_path)
all_PDB_filenames = get_PDB_filenames(origin_PDB_path)
all_object_names = get_object_names(origin_PDB_path)
# 催化活性中心所在文件夹
all_catalytic_core_dir = con_frag(root_dir, SASA_analysis_dir, catalytic_core_PDB_files_dir)
# 含溶剂分子的催化活性中心所在文件夹
all_catalytic_core_with_solvent_dir = con_frag(root_dir, SASA_analysis_dir, catalytic_core_PDB_files_dir_with_solvent)

# 设置字体
set_plot_font()
