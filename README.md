---
aliases: 
tags: 
authors: 
time: 2024-05-28T10:15:13
location: 
progress: 
version: 1
metaVersion: 1.1.0_20230310
---

# 项目文件使用教程

代码所在网址：[https://github.com/ADE150/Cas13a\_sensitivity\_research](https://github.com/ADE150/Cas13a_sensitivity_research)

## 文件使用

### 文件名缩写寓意

| 文件名单词 | 英文全称  | 备注                                |
| ---------: | :-------- | :---------------------------------- |
|        cal | calculate | 通过计算手段获得数据                |
|       plot | plot      | 将某数据绘制为（图表）              |
|        get | get       | 通过任何手段获得数据                |
|      bases | bases     | 碱基，一般指A(-3)/A(-4)碱基         |
|       resi | residue   | 残基                                |
|        dis | distance  | 碱基/残基的距离                     |
|      angle | angle     | 一般指A(-3)/A(-4)碱基之间的二面角   |
|     nearby | nearby    | 一般指A(-3)/A(-4)碱基附近的所有残基 |

### 文件作用与文件功能

以下标粗的为重要的文件夹与可用的Python脚本：

- **Python与PyMOL批量处理**/
    - .git/：版本管理文件夹
    - .gitattributes
    - .idea/
    - **00_install_pymol**/：安装PyMOL的文件夹
        - install_pymol.bat：安装PyMOL相关的文件
        - pymol-3.0.0-cp39-cp39-win_amd64.whl：安装PyMOL所需文件
        - pymol安装教程.txt
    - **01_get_Cas13a_designer**/：
        - 5xwp.cif：tgRNA-Cas13a野生型蛋白的结构文件
        - **A01_get_Cas13a_pdb.py**：获取两个Cas13a相关的结构文件并进行预处理
        - mt3.pdb
        - wt2.pdb
    - **02_molecular_dynamics_simulation**/
        - 40_PDB_files/：40个动力学模拟结果（PDB文件）
            - mt3_1.pdb
            - mt3_2.pdb
            - ……
            - mt3_20.pdb
            - wt2_1.pdb
            - wt2_2.pdb
            - ……
            - wt2_20.pdb
        - **A01_get_all_object.py**：获取40个PDB文件中的所有对象，并集中到一个文件中
        - par.mdin_分子动力学参数：分子动力学模拟时使用的参数
    - **03_SASA_analysis**/
        - **A01_get_catalytic_core_PDB.py**：将所有PDB文件的催化活性中心提取出来
        - **A02_cal_SASA_by_web.py**
        - **A03_cal_SASA_by_pymol.py**
        - **A04_plot_SASA.py**
        - **B01_get_two_SASA_with_solvent.py**
        - \_catalytic_core_PDB_files_with_solvent/：
        - catalytic_core_PDB_files/
            - mt3_1.pdb
            - mt3_2.pdb
            - ……
            - mt3_20.pdb
            - wt2_1.pdb
            - wt2_2.pdb
            - ……
            - wt2_20.pdb
    - **04_get_dis_bases_and_nearby**/：残基和附近碱基接触稳定性
        - A(-3)到963.png
        - A(-3)到967.png
        - A(-4)到963.png
        - A(-4)到967.png
        - **A01_cal_key_bases_and_resis.py**：cal_bases_nearby.py：计算A(-3)/A(-4)碱基到963和967的距离与二面角，distance_and_angle.xlsx文件中
        - **A02_plot_key_bases_and_resis.py**：读取表格，绘制极坐标图和时间演化图
        - **A03_show_dis_difference.py**
        - **B01_cal_bases_nearby.py**
        - distance_and_angle.xlsx
    - **05_已得到且已处理的数据文件**/
        - 01_get_Cas13a_designer/
            - 5xwp.cif
            - mt3.pdb
            - wt2.pdb
        - 02_molecular_dynamics_simulation/
            - MT3(20).png
            - WT2(20).png
            - all_origin_object.pse
        - 03_SASA_analysis/
            - SASA结果.xlsx
            - SASA结果_1.png
            - SASA结果_1.xlsx
            - SASA结果_2.png
            - SASA结果_2.xlsx
            - SASA结果_3.png
            - SASA结果_3.xlsx
            - SASA结果_上一次文件_pymol.xlsx
            - SASA结果_带溶剂_pymol.xlsx
            - init_SASA.txt
        - 04_get_dis_bases_and_nearby/
            - A(-3)与A(-4)附近的残基.xlsx
            - A(-3)到963.png
            - A(-3)到967.png
            - A(-4)到963.png
            - A(-4)到967.png
            - MT3(6)碱基与关键残基.png
            - WT2(6)碱基与关键残基.png
            - 碱基与关键残基的距离对比.pse
    - 06_trash/：过程文件和不再需要的代码
        - Deprecated/：已遗弃的代码文件
            - A02_caculate_d_and_angle.py
            - A03_get_nearby_resis.py
            - B02_caculate_distance_and_dihedral_angle.py
            - B03_contact_analysis_from_literature.py
            - cal_d_and_angle.py
            - distance_angle_evolution.png
            - gen_d_and_angle_plot.py
            - gen_d_and_angle_plot_single.py
            - other_functions.py
        - Temp_tools/
            - get_fiile_tree.py：生成文件树
            - print_page_num.py
        - Test/
            - C01_test_feature.py
            - compare_bat.py
            - flash_all_1.bat
            - flash_all_2.bat
            - test_cwd.py
        - Uncomplete_data/
            - distance_and_angle.xlsx
            - distance_angle_plot.png
        - 便捷的pymol指令.txt
    - \_\_pycache\_\_/
    - **common_tools.py**：工具类，将常用函数提取至此处，提高代码维护性与可塑性
    - README.md：项目文件使用教程的Markdown文件
    - 项目文件使用教程.pdf

## 注意事项

1. 在运行任何Python脚本文件前，一定要将root_dir的路径改为该项目所在路径，如：`C:\Users\297\Downloads\Cas13a_sensitivity_research`，最后一个文件夹不用加`\`号。
2. 计算类代码（名字带有「cal」的）需要保证所需PDB文件在原目录中，若需要移动，则需要更改common_tools下对应的变量
3. 绘图类代码需要在计算类代码运行完成，并且生成数据后使用！
4. 如果代码长时间未响应，可使用断点调试查看变量的运行值，或者使用插入多个print方法确定进度，考虑运行时间与电脑配置和环境有关，
5. 如果需要运行「SASA计算平台」计算代码，则需要安装用于自动操控浏览器的Edge驱动。请到[Microsoft Edge WebDriver | Microsoft Edge Developer](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads)下载Edge浏览器的webdriver，并且将其安装目录添加到环境变量后再运行相关的代码
6. 代码仅供学习，需要完成其他用途请联系本人

如果对代码有问题，可加QQ联系：3185639982，并备注来意「Cas13a」。







