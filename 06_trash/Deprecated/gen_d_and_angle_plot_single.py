from common_tools import *

# 解决一次性生成多张图片出现数据混乱，数据无法读取的问题

excel_path= "../../04_get_dis_bases_and_nearby/distance_and_angle.xlsx"

workbook = openpyxl.load_workbook(excel_path)

# 获取所有表名
sheet_names = workbook.sheetnames



sheet_name=sheet_names[1]

df=pd.read_excel(excel_path, sheet_name=sheet_name)
# 提取数据
objects = df[df.columns[0]]
distances = df[df.columns[1]]
# distances= pd.to_numeric(distances, errors='coerce')
print_stack_trace(distances)
angles = df[df.columns[2]]
# 将数据分为WT2和MT3两组
wt2_distances = []
mt3_distances = []
wt2_angles = []
mt3_angles = []

for obj,dist,angle in zip(objects,distances,angles):
    if obj.startswith('wt2'):
        wt2_distances.append(dist)
        wt2_angles.append(angle)
    elif obj.startswith('mt3'):
        mt3_distances.append(dist)
        mt3_angles.append(angle)
# 创建极坐标图
fig=plt.figure(figsize=(14, 7))

# 清理旧数据
# plt.clf()  # 在创建新图形之前清除当前的图形

ax1=fig.add_subplot(121, projection='polar')

# 设置极坐标图网格线的颜色
ax1.grid(color='#f0f0f0', linewidth=1.75)
# 设置极坐标图外围圆的颜色
ax1.spines['polar'].set_edgecolor('#f0f0f0')
# 将角度转换为弧度
wt2_angles_rad = np.deg2rad(wt2_angles)
mt3_angles_rad = np.deg2rad(mt3_angles)

# 绘制极坐标图
ax1.scatter(wt2_angles_rad, wt2_distances, color='#bebebe', label='WT2')
ax1.scatter(mt3_angles_rad, mt3_distances, color='#3fe0d0', label='MT3')

# 设置极坐标网格
ax1.set_rmax(6)
# ax1.set_rticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
ax1.set_rticks([2, 4, 6])
ax1.set_theta_zero_location('E')  # 0°在右边
ax1.set_thetamin(-180)  # 设置极坐标的最小角度
ax1.set_thetamax(180)  # 设置极坐标的最大角度
ax1.set_thetagrids(range(-180, 180, 45))  # 显示角度网格

ax1.grid(True)
ax1.set_title("Polar Plot of Distance and Dihedral Angle")

# 创建时间演化图
times = np.arange(0, 100, 5)  # 每帧间隔5ps，共20帧，跨度为100ps

ax2=fig.add_subplot(222)
ax3=fig.add_subplot(224)

# 绘制距离随时间变化的图
ax2.plot(times, wt2_distances, color='#bebebe', label='WT2')
ax2.plot(times, mt3_distances, color='#3fe0d0', label='MT3')
ax2.set_xlabel("Time / ps")
ax2.set_ylabel("Distance d / Å")
ax2.set_ylim(2, 6)
ax2.set_title("Distance Evolution Over Time")
ax2.legend()

# 绘制角度随时间变化的图
ax3.plot(times, wt2_angles, color='#bebebe', label='WT2')
ax3.plot(times, mt3_angles, color='#3fe0d0', label='MT3')
ax3.set_xlabel("Time / ps")
ax3.set_ylabel("Angle θ / °")
ax3.set_ylim(-120, -60)
ax3.set_title("Angle Evolution Over Time")
ax3.legend()

# 调整布局和边距
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)

# 调整布局
# plt.tight_layout()
plt.savefig(f"{sheet_name}.png")
plt.show()



