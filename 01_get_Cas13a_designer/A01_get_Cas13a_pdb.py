from common_tools import *

wt2="wt2"
mt3="mt3"
# 获取WT2
pymol_cmd.fetch("5XWP")
pymol_cmd.set_name("5XWP",wt2)
# 删除溶剂分子
remove_solvent()
# 将二聚体结构处理为单聚体
select_and_remove(f"{wt2} and (chain B or chain E or chain F)")
# 创造MT3对象
pymol_cmd.copy_to(mt3,wt2)
# 选择A链第967位的酪氨酸
pymol_cmd.select("target_residue", f"{mt3} and chain A and resi 967 and resn TYR")
# 启动突变向导并设置模式为精氨酸
pymol_cmd.wizard("mutagenesis")
pymol_cmd.get_wizard().set_mode("ARG")
# 选择要突变的残基
pymol_cmd.get_wizard().do_select("target_residue")
# 应用突变
pymol_cmd.get_wizard().apply()
# 结束向导
pymol_cmd.set_wizard()

pymol_cmd_save("wt2.pdb",wt2)
pymol_cmd_save("mt3.pdb",mt3)

pymol_cmd.quit()








