"""
将所有原始PDB文件加载到同一个窗口，并以文件名作为对象
"""
from common_tools import *

remind_start("加载PDB文件至窗口")

for pos in range(len(all_PDB_paths)):
    the_object_name = all_object_names[pos]
    load_no_solvent(all_PDB_paths, the_object_name)
    pymol_cmd.disable(the_object_name)
    # 输出当前正在处理的对象
    remind_detail(the_object_name)

remind_start("保存文件")
pymol_cmd_save(all_origin_object_path)
remind_start("关闭窗口")
pymol_cmd.quit()



