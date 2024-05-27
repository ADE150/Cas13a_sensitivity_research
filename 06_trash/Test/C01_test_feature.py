import os

from common_tools import *
import pandas as pd

# 想要测试model.atom会读取到什么东西

pymol.finish_launching()
PDB_filenames= [f for f in os.listdir(origin_PDB_path) if f.endswith(".pdb")]
PDB_filenames.sort(key=lambda x: (x[:3], int(find_first_str(x, r"_(.+?)\.pdb"))))
the_filename=PDB_filenames[0]
the_object_name=os.path.splitext(PDB_filenames[0])[0]

pymol_cmd.load(con_frag(origin_PDB_path, the_filename))
A_3_resi="A_-3_resi"
A_3_resi_CA="A_-3_resi_CA"
Y967="Y967"
remove_solvent()
nearby="A_-3_nearby_5"
pymol_cmd.select(A_3_resi,f"object {the_object_name} and chain B and resi 27")
pymol_cmd.select(A_3_resi_CA,f"object {the_object_name} and chain B and resi 27 and name CA")
pymol_cmd.select(Y967,f"object {the_object_name} and chain A and resi 967")
# pymol_cmd.select(A_3_resi,f"{the_object_name}//B/27")
pymol_cmd.select(nearby,f"object {the_object_name} and br. {A_3_resi} around 7 and not {A_3_resi} and name CA")

test_dis=pymol_cmd.distance("test_dis",A_3_resi,Y967)

print_stack_trace(test_dis)

sleep(300)

# 创建一个空的数据框列表
data_27 = []
data_28 = []


# 定义选择半径
distances = [1, 2, 3, 4, 5]

# 定义要处理的残基和链
residues = [(27, 'B', 'A'), (28, 'B', 'A')]

model=pymol_cmd.get_model(nearby)



added_residues=set()

for atom in model.atom:
    residue_identifier = (atom.chain, atom.resi)
    if residue_identifier not in added_residues:
        # 计算最近距离
        target_atom = pymol_cmd.get_model(A_3_resi).atom[0]
        distance = pymol_cmd.get_distance(A_3_resi, f"{the_object_name}//{atom.chain}/{atom.resi}/{atom.name}")

        # 记录数据
        record = {
            'Object': the_object_name,
            'Chain': atom.chain,
            'Residue': atom.resi,
            'Sequence Position': atom.resi,
            'Residue Name': atom.resn,
            'cmd_distance': 7,
            'distance': distance
        }
        data_27.append(record)
        # if resi == 27:
        #     data_27.append(record)
        # else:
        #     data_28.append(record)

        added_residues.add(residue_identifier)

df_27 = pd.DataFrame(data_27)

print(df_27)

    # 清理选择
# pymol_cmd.delete('target')
# pymol_cmd.delete('nearby')


# 从pse文件读取对象名
# pymol.finish_launching()
#
# pymol_cmd.load(all_origin_object_filename)
#
# catalytic_core_object_names=pymol_cmd.get_object_list()
#
# print_stack_trace(catalytic_core_object_names)




























