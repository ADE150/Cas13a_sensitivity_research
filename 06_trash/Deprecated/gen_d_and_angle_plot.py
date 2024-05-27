
from common_tools import *


# 解决一次性生成多张图片出现数据混乱，数据无法读取的问题

excel_path= "../../04_get_dis_bases_and_nearby/distance_and_angle.xlsx"


# 指定字体路径
font_path = r'C:\Windows\Fonts\PingFang SC.ttf'  # 替换为实际字体文件路径
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = [font_prop.get_name()] # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
# 设置中文字体
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
# plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

workbook = openpyxl.load_workbook(excel_path)

# 获取所有表名
sheet_names = workbook.sheetnames

figs=[]


# pos=0

for sheet_name in sheet_names:
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
    figs.append(fig)

    # 计算显示的最小值和最大值
    min_value=min(min(wt2_distances),min(mt3_distances))
    max_value=max(max(wt2_distances),max(mt3_distances))
    ax_dis_min=math.floor(min_value)
    ax_dis_max=math.ceil(max_value)+2

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
    ax1.set_rmax(ax_dis_max)
    # ax1.set_rticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
    ax1.set_rticks(list(range(2,ax_dis_max,2)))
    ax1.set_theta_zero_location('E')  # 0°在右边
    ax1.set_thetamin(-180)  # 设置极坐标的最小角度
    ax1.set_thetamax(180)  # 设置极坐标的最大角度
    ax1.set_thetagrids(range(-180, 180, 45))  # 显示角度网格

    ax1.grid(True)
    # ax1.set_title("Polar Plot of Distance and Dihedral Angle")
    ax1.set_title("距离与二面角极坐标图")

    # 创建时间演化图
    times = np.arange(0, 100, 5)  # 每帧间隔5ps，共20帧，跨度为100ps

    ax2=fig.add_subplot(222)
    ax3=fig.add_subplot(224)

    # 绘制距离随时间变化的图
    ax2.plot(times, wt2_distances, color='#bebebe', label='WT2')
    ax2.plot(times, mt3_distances, color='#3fe0d0', label='MT3')
    ax2.set_xlabel("Time / ps")
    ax2.set_ylabel("Distance d / Å")
    ax2.set_ylim(ax_dis_min, ax_dis_max)
    # ax2.set_title("Angle Evolution Over Time")
    ax2.set_title("距离时间演化图")
    ax2.legend()

    # 绘制角度随时间变化的图
    ax3.plot(times, wt2_angles, color='#bebebe', label='WT2')
    ax3.plot(times, mt3_angles, color='#3fe0d0', label='MT3')
    ax3.set_xlabel("Time / ps")
    ax3.set_ylabel("Angle θ / °")
    ax3.set_ylim(-120, -60)
    # ax3.set_title("Angle Evolution Over Time")
    ax3.set_title("角度时间演化图")
    ax3.legend()

    # 调整布局和边距
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)

    # 调整布局
    # plt.tight_layout()
    plt.savefig(f"{sheet_name}.png")

# 显示图表，并在30s后自动关闭
plt.show()
sleep(30)
close_all_fig(figs)


#
#
# # 对象集合文件的文件路径
# output_all_object_dir = connect_dir(intermediate_products_dir, distance_and_angle_folder + r"\all_object.pdb")
# # 「选择附近残基」文件的文件路径
# output_resis_around_object_dir = connect_dir(intermediate_products_dir,
#                                              distance_and_angle_folder + r"\resis_around.pdb")
# # 距离和二面角结果的文件路径
# output_distance_and_angle_result_dir = connect_dir(output_dir,
#                                                    distance_and_angle_folder + r"\distance_and_angle.xlsx")
#
#
#
#
# # 读取Excel文件
# # filename = 'distances_and_angles.xlsx'
# filename = output_distance_and_angle_result_dir
# workbook = openpyxl.load_workbook(filename)
# worksheet = workbook.active
#
# # 提取数据
# objects = []
# distances = []
# angles = []
#
#
#
# for row in worksheet.iter_rows(min_row=2, values_only=True):
#     objects.append(row[0])
#     distances.append(row[1])
#     angles.append(row[2])
#
# # 将数据分为WT2和MT3两组
# wt2_distances = []
# mt3_distances = []
# wt2_angles = []
# mt3_angles = []
#
# for the_object, dist, angle in zip(objects, distances, angles):
#     if the_object.startswith('wt2'):
#         wt2_distances.append(dist)
#         wt2_angles.append(angle)
#     elif the_object.startswith('mt3'):
#         mt3_distances.append(dist)
#         mt3_angles.append(angle)
#
# # 创建极坐标图
# plt.figure(figsize=(14, 7))
#
# ax1 = fig.add_subplot(121, projection='polar')
#
# # 设置极坐标图网格线的颜色
# ax1.grid(color='#f0f0f0',linewidth=1.75)
# # 设置极坐标图外围圆的颜色
# ax1.spines['polar'].set_edgecolor('#f0f0f0')
# # 将角度转换为弧度
# wt2_angles_rad = np.deg2rad(wt2_angles)
# mt3_angles_rad = np.deg2rad(mt3_angles)
#
# # 绘制极坐标图
# ax1.scatter(wt2_angles_rad, wt2_distances, color='#bebebe', label='WT2')
# ax1.scatter(mt3_angles_rad, mt3_distances, color='#3fe0d0', label='MT3')
#
# # 设置极坐标网格
# ax1.set_rmax(6)
# # ax1.set_rticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
# ax1.set_rticks([2,4,6])
# ax1.set_theta_zero_location('E')  # 0°在右边
# ax1.set_thetamin(-180)  # 设置极坐标的最小角度
# ax1.set_thetamax(180)  # 设置极坐标的最大角度
# ax1.set_thetagrids(range(-180, 180, 45))  # 显示角度网格
#
# ax1.grid(True)
# ax1.set_title("Polar Plot of Distance and Dihedral Angle")
#
# # 创建时间演化图
# times = np.arange(0, 100, 5)  # 每帧间隔5ps，共20帧，跨度为100ps
#
# ax2 = fig.add_subplot(222)
# ax3 = fig.add_subplot(224)
#
# # 绘制距离随时间变化的图
# ax2.plot(times, wt2_distances, color='#bebebe', label='WT2')
# ax2.plot(times, mt3_distances, color='#3fe0d0', label='MT3')
# ax2.set_xlabel("Time / ps")
# ax2.set_ylabel("Distance d / Å")
# ax2.set_ylim(2, 6)
# ax2.set_title("Distance Evolution Over Time")
# ax2.legend()
#
# # 绘制角度随时间变化的图
# ax3.plot(times, wt2_angles, color='#bebebe', label='WT2')
# ax3.plot(times, mt3_angles, color='#3fe0d0', label='MT3')
# ax3.set_xlabel("Time / ps")
# ax3.set_ylabel("Angle θ / °")
# ax3.set_ylim(-120, -60)
# ax3.set_title("Angle Evolution Over Time")
# ax3.legend()
#
# # 调整布局和边距
# plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)
#
# # 调整布局
# # plt.tight_layout()
# output_distance_and_angle_result_plot_dir=connect_dir(os.path.dirname(output_distance_and_angle_result_dir),r"distance_angle_plot.png")
# print_stack_trace(output_distance_and_angle_result_plot_dir)
# plt.savefig(output_distance_and_angle_result_plot_dir)
# plt.show()





