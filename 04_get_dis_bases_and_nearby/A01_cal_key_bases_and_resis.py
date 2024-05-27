from common_tools import *

output_d_and_a_dir="cal_key_bases_and_resis.xlsx"

# A(-3)和A(-4)碱基
resis_1=[("B","28"),("B","27")]
# 963和967
resis_2=[("A","963"),("A","967")]

# 测试数据
# B28_963_distance=[1,2,3,4,5]
# B28_967_distance=[6,7,8,9,10]
# B27_963_distance=[11,12,13,14,15]
# B27_967_distance=[16,17,18,19,20]
# B28_B27_angle=[90,91,92,93,94]

B28_963_distance=[]
B28_967_distance=[]
B27_963_distance=[]
B27_967_distance=[]
B28_B27_angle=[]

def save_distance(distance,resi_1,resi_2):
    if resi_1==28 and resi_2==963:
        B28_963_distance.append(distance)
    elif resi_1==28 and resi_2==967:
        B28_967_distance.append(distance)
    elif resi_1==27 and resi_2==963:
        B27_963_distance.append(distance)
    elif resi_1==27 and resi_2==967:
        B27_967_distance.append(distance)
    else:
        print_stack_trace("警告：出现不明残基数据！")

for n in range(len(all_PDB_paths)):
    pymol_cmd.load(all_PDB_paths[n])
    object_name=all_object_names[n]
    # 判断是否为突变体
    # is_mutant=True if object_name.startswith("mt") else False

    # 计算碱基之间的二面角
    # 选择链B 27位A碱基的C3'原子
    atom_B27_C3 = f'object {object_name} and chain B and resi 27 and name C3\''
    # 选择链B 28位A碱基的C3'原子
    atom_B28_C3 = f'object {object_name} and chain B and resi 28 and name C3\''
    # 选择链B 27位A碱基的C8原子
    atom_B27_C8 = f'object {object_name} and chain B and resi 27 and name C8'
    # 选择链B 27位A碱基的C2原子
    atom_B27_C2 = f'object {object_name} and chain B and resi 27 and name C2'
    # 计算二面角 θ
    dihedral_angle = pymol_cmd.get_dihedral(atom_B27_C3, atom_B28_C3, atom_B27_C8, atom_B27_C2)
    B28_B27_angle.append(dihedral_angle)
    for chain_1,resi_1 in resis_1:
        for chain_2,resi_2 in resis_2:
            # 计算碱基与残基的距离
            resi_1_name = f"{object_name}_resi_1"
            resi_2_name=f"{object_name}_resi_2"
            # 碱基的质心
            pymol_cmd.select(resi_1_name, f"object {object_name} and chain {chain_1} and resi {resi_1} and name N1+C6")
            # 残基的Cα原子
            pymol_cmd.select(resi_2_name, f"object {object_name} and chain {chain_2} and resi {resi_2} and name CA")
            virtual_atom_name="virtual_atom"
            pymol_cmd.pseudoatom(virtual_atom_name,selection=resi_1_name)
            # 保存距离和二面角到特定的表里
            distance=pymol_cmd.get_distance(resi_2_name,virtual_atom_name)
            save_distance(distance,int(resi_1),int(resi_2))
            # 清除当前选中，防止选中对象干扰下一步计算，并节省内存
            pymol_cmd.delete(resi_1_name)
            pymol_cmd.delete(resi_2_name)
            pymol_cmd.remove(virtual_atom_name)
            pymol_cmd.delete(distance)
    remove_selection()

# workbook = openpyxl.Workbook()
# workbook.remove(workbook.active)

sheet_data={
    "A(-4)到963":B28_963_distance,
    "A(-4)到967":B28_967_distance,
    "A(-3)到963":B27_963_distance,
    "A(-3)到967":B27_967_distance
}

temp=[]

for sheet_name,distance in sheet_data.items():
    data={
        "Object":all_object_names,
        "Distance":distance,
        "Angle":B28_B27_angle
    }
    temp.append((sheet_name,data))
write_multi_sheet_to_excel_1(output_d_and_a_dir,*temp)

# 测试用
# for sheet_name, distances in sheet_data.items():
#     df = pd.DataFrame({
#         "object": ["a","b","c","d","e"],
#         "distance": distances,
#         "angle": B28_B27_angle
#     })

# 原有的Excel保存方式
# for sheet_name,distances in sheet_data.items():
#     df=pd.DataFrame({
#         "object":all_object_names,
#         "distance":distances,
#         "angle":B28_B27_angle
#     })
#
#
#     sheet = workbook.create_sheet(title=sheet_name)
#     for r in dataframe_to_rows(df, index=False, header=True):
#         sheet.append(r)
#
#     # # 将 DataFrame 写入新的表
#     # with pd.ExcelWriter(output_d_and_a_dir, engine='openpyxl', mode='a') as writer:
#     #     df.to_excel(writer, sheet_name=sheet_name, index=False)
#
# workbook.save(output_d_and_a_dir)



