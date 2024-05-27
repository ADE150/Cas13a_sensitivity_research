import os
import pymol
import time
import matplotlib.pyplot as plt
from common_tools import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pymol_cmd = pymol.cmd
import numpy as np
import matplotlib.pyplot as plt

# 加载PDB文件
pdb_file = 'your_pdb_file.pdb'
pymol_cmd.load(pdb_file)

# 定义计算质心的函数
def compute_centroid(selection):
    model = pymol_cmd.get_model(selection)
    atoms = model.atom
    positions = np.array([atom.coord for atom in atoms])
    centroid = np.mean(positions, axis=0)
    return centroid

# 选择需要计算质心和二面角的原子
ca_963 = 'resi 963 and name CA'
a_3_base = 'resi -3 and name N1+C6'
atom1 = 'resi -4 and name C3\''
atom2 = 'resi -3 and name C3\''
atom3 = 'resi -4 and name C8'
atom4 = 'resi -4 and name C2'

# 计算质心距离
centroid_ca_963 = compute_centroid(ca_963)
centroid_a_3_base = compute_centroid(a_3_base)
distance = np.linalg.norm(centroid_ca_963 - centroid_a_3_base)

print(f'Distance between C⍺ atom at position 963 and A(-3) base centroid: {distance:.2f} Å')

# 计算二面角
dihedral_angle = pymol_cmd.get_dihedral(atom1, atom2, atom3, atom4)
print(f'Dihedral angle: {dihedral_angle:.2f} degrees')

# 绘制极坐标图
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.scatter(np.radians(dihedral_angle), distance, c='r', label='Mutant Data')
# 假设你有WT数据，可以替换以下内容
# ax.scatter(np.radians(dihedral_angle_wt), distance_wt, c='gray', label='WT Data')

ax.set_title('Conformational Dynamics of A(-3)')
ax.set_xlabel('Angle (degrees)')
ax.set_ylabel('Distance (Å)')
ax.legend()
plt.show()

