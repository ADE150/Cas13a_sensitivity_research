from common_tools import *

# 获取有溶剂分子的文件

pymol.finish_launching()

remind_start("获取催化活性中心")

# 获取每个PDB文件中的催化活性中心（第470-480位和1045-1055位残基）
for n in range(len(all_PDB_paths)):
    the_path=all_PDB_paths[n]
    the_object=all_object_names[n]
    remind_detail(f"正在获取{the_object}的活性中心")
    the_catalytic_core_name=f"{the_object}_cc"
    pymol_cmd.load(the_path, the_object)
    # 不去除溶剂分子将其对SASA数值的影响计入结果
    # remove_solvent()
    pymol_cmd.disable(the_object)
    # 选择残基
    pymol_cmd.select(the_catalytic_core_name,f"object {the_object} and chain A and (resi 470-480 or resi 1045-1055)")
    save_path=con_frag(all_catalytic_core_with_solvent_dir, f"{the_object}.pdb")
    pymol_cmd_save(save_path,the_catalytic_core_name)
    # 清理数据，准备加载下一个文件
    remove_selection()

remind_end("获取催化活性中心的PDB文件")

# 所有PDB文件的文件路径
catalytic_core_PDB_paths = get_PDB_paths(all_catalytic_core_with_solvent_dir)

# 暂时保存SASA结果
results_by_web = []
results_by_pymol=[]
# 初始化 WebDriver
open_edge()
wait = WebDriverWait(web_edge_driver, 30)  # 设置显式等待的最长时间为30秒

# 打开目标网站
url = "https://www.novopro.cn/tools/calculate-solvent-accessible-surface-area.html"
web_edge_driver.get(url)

# 遍历所有PDB文件
for pdb_file in catalytic_core_PDB_paths:
    try:
        # 找到文件上传元素并上传文件
        upload_element = wait.until(EC.presence_of_element_located((By.ID, "pdb_file")))
        upload_element.send_keys(pdb_file)

        # 找到并点击提交按钮
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "input-design-submit")))
        submit_button.click()

        # 等待计算结果，最多等待10秒
        result_element = wait.until(EC.visibility_of_element_located((By.ID, "05_已得到且已处理的数据文件-res")))
        sleep(15)  # 根据需要调整等待时间
        result_text = result_element.text

        # 提取溶剂可及表面积结果
        if "溶剂可及表面积" in result_text:
            sasa = result_text.split(":")[1].strip()
            print(f"{pdb_file}：{sasa}")
            results_by_web.append({"Object": pdb_file, "SASA": sasa})
        else:
            print(f" {pdb_file} SASA获取失败")
            results_by_web.append({"Object": pdb_file, "SASA": "无法获取"})
        # 清除上传的文件，刷新页面
        web_edge_driver.refresh()
    except Exception as e:
        print(f"Error processing {pdb_file}: {e}")
        results_by_web.append({"Object": pdb_file, "SASA": f"错误：{e}"})

# 关闭 WebDriver
web_edge_driver.quit()
# 写入结果
write_to_excel("SASA_with_solvent_by_web.xlsx", results_by_web)

catalytic_core_object_names=get_object_names(all_catalytic_core_with_solvent_dir)

for n in range(len(catalytic_core_PDB_paths)):
    the_path=catalytic_core_PDB_paths[n]
    the_object=catalytic_core_object_names[n]
    # 所属的对象的名字
    the_subject=all_object_names[n]
    pymol_cmd.load(the_path,the_object)
    SASA=pymol_cmd.get_area(the_object)
    results_by_pymol.append({"Object":the_subject,"SASA":SASA})
    # 清除数据，准备计算下一个数据
    remove_selection()

write_to_excel("SASA_with_solvent_by_pymol.xlsx",results_by_pymol)

pymol_cmd.quit()


























