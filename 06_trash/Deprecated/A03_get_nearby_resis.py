from common_tools import *

import pandas as pd
import numpy as np

pymol.finish_launching()

# 加载Pymol文件
pse_file =all_origin_object_filename
pymol_cmd.load(pse_file)
output_file = con_frag(output_dir + rf"\{nearby_resis_folder}", "A(-3)与A(-4)附近的残基.xlsx")


# 创建一个空的数据框列表
data_27 = []
data_28 = []

# 定义选择半径
distances = [1, 2, 3, 4, 5]

# 定义要处理的残基和链
residues = [(27, 'B', 'A'), (28, 'B', 'A')]

# from pymol import cmd
# import pandas as pd
#
# # 加载Pymol文件
# pse_file = 'o_path/to/your/file.pse'
# pymol_cmd.load(pse_file)
#
# 创建一个空的数据框列表
# data_27 = []
# data_28 = []
#
# # 定义选择半径
# distances = [1, 2, 3, 4, 5]
#
# # 定义要处理的残基和链
# residues = [(27, 'B'), (28, 'B')]

# 获取所有对象的名称
# object_list = pymol_cmd.get_object_list('*')
object_list = pymol_cmd.get_object_list()

# 遍历所有对象和指定残基
for obj in object_list:
    print(f"Processing object: {obj}")
    for resi, chain,resn_name in residues:
        for cmd_distance in distances:
            # 选择目标残基
            target_selection = f"/{obj}//{chain}/{resi}"
            print(f"Selecting: {target_selection}")
            pymol_cmd.select('target', target_selection)

            # 检查选择是否成功
            target_count = pymol_cmd.count_atoms('target')
            if target_count == 0:
                print(f"Error: Failed to select target residue {resi} in chain {chain} of object {obj}")
                continue
            else:
                print(f"Selected {target_count} atoms in target residue {resi} in chain {chain} of object {obj}")

            # 选择目标残基附近指定距离内的其他残基
            nearby_selection = f"br. (target around {cmd_distance}) and not (resn A and resi {resi})"
            pymol_cmd.select('nearby', nearby_selection)

            # 获取选择的残基信息
            nearby_model = pymol_cmd.get_model('nearby')

            # 使用集合来跟踪已经添加的残基
            added_residues = set()

            for nearby_atom in nearby_model.atom:
                residue_identifier = (nearby_atom.chain, nearby_atom.resi)
                if residue_identifier not in added_residues:
                    # 计算target与nearby的平均距离
                    sel_2=f"/{obj}//{nearby_atom.chain}/{nearby_atom.resi}"
                    sel_2_index=f"index {nearby_atom.index}"
                    distance_name=f'dis_{obj}_{nearby_atom.resi}_'
                    distance = pymol_cmd.distance(distance_name,'target',sel_2)

                    # 记录数据
                    record = {
                        'Object': obj,
                        'Chain': nearby_atom.chain,
                        'Residue': nearby_atom.resi,
                        'Sequence Position': nearby_atom.resi,
                        'Residue Name': nearby_atom.resn,
                        'cmd_distance': cmd_distance,
                        'distance': distance  # 保存平均距离
                    }

                    if resi == 27:
                        data_27.append(record)
                    else:
                        data_28.append(record)

                    added_residues.add(residue_identifier)
                    pymol_cmd.delete(distance_name)

            print(f"Distance for residue {resi} in chain {chain} with cmd_distance {cmd_distance} is: {distance} Å")

            # 清理选择
            pymol_cmd.delete('target')
            pymol_cmd.delete('nearby')

# 将数据转换为数据框
df_27 = pd.DataFrame(data_27)
df_28 = pd.DataFrame(data_28)

# 将数据框保存为Excel文件，不同表分别记录27位和28位残基的信息
# output_file = '05_已得到且已处理的数据文件.xlsx'
with pd.ExcelWriter(output_file) as writer:
    df_27.to_excel(writer, sheet_name='A(-4)', index=False)
    df_28.to_excel(writer, sheet_name='A(-3)', index=False)

pymol_cmd.quit()

# ——————————————————————

# # 遍历所有对象
# object_list = pymol_cmd.get_object_list()
# 
# # 遍历所有对象和指定残基
# for n in object_list:
#     remind_detail(n)
#     for resi, chain, resn in residues:
#         for cmd_distance in distances:
#             # 选择目标残基
#             target_selection = f"{n}//{chain}/{resi}"
#             pymol_cmd.select('target', target_selection)
# 
#             # 选择目标残基附近指定距离内的其他残基
#             nearby_selection = f"br. (target around {cmd_distance}) and not (resn {resn} and resi {resi})"
#             pymol_cmd.select('nearby', nearby_selection)
# 
#             # 获取选择的残基信息
#             model = pymol_cmd.get_model('nearby')
# 
#             # 使用集合来跟踪已经添加的残基
#             added_residues = set()
# 
#             for atom in model.atom:
#                 residue_identifier = (atom.chain, atom.resi)
#                 if residue_identifier not in added_residues:
#                     # 计算最近距离
#                     target_atom = pymol_cmd.get_model('target').atom[0]
#                     distance = pymol_cmd.get_distance('target', f"{n}//{atom.chain}/{atom.resi}/{atom.name}")
# 
#                     # 记录数据
#                     record = {
#                         'Object': n,
#                         'Chain': atom.chain,
#                         'Residue': atom.resi,
#                         'Sequence Position': atom.resi,
#                         'Residue Name': atom.resn,
#                         'cmd_distance': cmd_distance,
#                         'distance': distance
#                     }
# 
#                     if resi == 27:
#                         data_27.append(record)
#                     else:
#                         data_28.append(record)
# 
#                     added_residues.add(residue_identifier)
# 
#             # 清理选择
#             pymol_cmd.delete('target')
#             pymol_cmd.delete('nearby')
# 
# # 将数据转换为数据框
# df_27 = pd.DataFrame(data_27)
# df_28 = pd.DataFrame(data_28)
# 
# # 将数据框保存为Excel文件，不同表分别记录27位和28位残基的信息
# # output_file = '05_已得到且已处理的数据文件.xlsx'
# with pd.ExcelWriter(output_file) as writer:
#     df_27.to_excel(writer, sheet_name='A(-3)', index=False)
#     df_28.to_excel(writer, sheet_name='A(-4)', index=False)









