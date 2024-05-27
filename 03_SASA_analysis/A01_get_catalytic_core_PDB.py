from common_tools import *

pymol.finish_launching()

remind_start("获取催化活性中心")

# 获取每个PDB文件中的催化活性中心（第470-480位和1045-1055位残基）
for n in range(len(all_PDB_paths)):
    the_path=all_PDB_paths[n]
    the_object=all_object_names[n]
    remind_detail(f"正在获取{the_object}的活性中心")
    # 给催化活性中心对象随便取个名字
    the_catalytic_core_name=f"{the_object}_cc"
    load_no_solvent(the_path, the_object)
    pymol_cmd.disable(the_object)
    # 选择残基
    pymol_cmd.select(the_catalytic_core_name,f"object {the_object} and chain A and (resi 470-480 or resi 1045-1055)")
    save_path=con_frag(all_catalytic_core_dir,f"{the_object}.pdb")
    pymol_cmd_save(save_path,the_catalytic_core_name)
    # 清理数据，准备加载下一个文件
    remove_selection()

remind_end("获取催化活性中心的PDB文件")

pymol_cmd.quit()



