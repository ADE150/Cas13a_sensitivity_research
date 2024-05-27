from common_tools import *

# 所有PDB文件的文件路径
catalytic_core_PDB_paths = get_PDB_paths(all_catalytic_core_dir)

# 暂时保存SASA结果
results = []
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
            results.append({"Object": pdb_file, "SASA": sasa})
        else:
            print(f" {pdb_file} SASA获取失败")
            results.append({"Object": pdb_file, "SASA": "无法获取"})
        # 清除上传的文件，刷新页面
        web_edge_driver.refresh()
    except Exception as e:
        print(f"Error processing {pdb_file}: {e}")
        results.append({"Object": pdb_file, "SASA": f"错误：{e}"})

# 关闭 WebDriver
web_edge_driver.quit()
# 写入结果
write_to_excel("SASA_by_web.xlsx",results)


