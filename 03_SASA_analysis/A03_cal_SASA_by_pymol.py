from common_tools import *

results = []
catalytic_core_PDB_paths=get_PDB_paths(all_catalytic_core_dir)
catalytic_core_object_names=get_object_names(all_catalytic_core_dir)

for n in range(len(catalytic_core_PDB_paths)):
    the_path=catalytic_core_PDB_paths[n]
    the_object=catalytic_core_object_names[n]
    # 所属的对象的名字
    the_subject=all_object_names[n]
    pymol_cmd.load(the_path,the_object)
    SASA=pymol_cmd.get_area(the_object)
    results.append({"Object":the_subject,"SASA":SASA})
    # 清除数据，准备计算下一个数据
    remove_selection()

write_to_excel("SASA_by_pymol.xlsx",results)

pymol_cmd.quit()






