from common_tools import *

"""
该脚本可计算A(-3)与A(-4)附近的所有残基，并汇总到一个工作簿中（含两个工作表）
"""
pymol.finish_launching()

output_file =r"关键碱基附近残基的信息\A(-3)与A(-4)附近的所有残基.xlsx"

# 创建一个空的数据框列表
data_27 = []
data_28 = []

# 输入想要计算的距离，填写多个距离将全部计算，可能会出现重复结果，如：
# 距离为5的结果（残基）中，一定会有距离为1,2,3,4的结果（残基）
# distances = [1, 2, 3, 4, 5]
distances = [5]

# 定义要处理的残基和链
residues = [(27, 'B', 'A'), (28, 'B', 'A')]

object_list = pymol_cmd.get_object_list()

# 遍历所有对象和指定残基
for the_object,the_path in all_object_names,all_PDB_paths:
    load_no_solvent(the_path,the_object)
    remind_detail(f"正在处理对象：{the_object}")
    for resi, chain,resn_name in residues:
        for cmd_distance in distances:
            # 选择目标残基
            target_selection = f"/{the_object}//{chain}/{resi}"
            # print_stack_trace(f"Selecting: {target_selection}")
            pymol_cmd.select('target', target_selection)

            # 检查选择是否成功
            # target_count = pymol_cmd.count_atoms('target')
            # if target_count == 0:
            #     print(f"错误-加载失败：select target residue {resi} in chain {chain} of object {the_object}")
            #     continue
            # else:
            #     print(f"已选择 {target_count} atoms in target residue {resi} in chain {chain} of object {the_object}")

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
                    sel_2=f"/{the_object}//{nearby_atom.chain}/{nearby_atom.resi}"
                    sel_2_index=f"index {nearby_atom.index}"
                    distance_name=f'dis_{the_object}_{nearby_atom.resi}_'
                    distance = pymol_cmd.distance(distance_name,'target',sel_2)

                    # 记录数据
                    record = {
                        'Object': the_object,
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

# 将数据保存到表格中
write_multi_sheet_to_excel_1(output_file,
                             ("A(-4)",data_27),
                             ("A(-3)",data_28))

pymol_cmd.quit()


