import os

from common_tools import *

# 读取当前文件夹的所有Excel文件
excel_paths=get_cwd_excels()
# excel_paths=["SASA_by_web.xlsx"]

figs=[]

for excel_path in excel_paths:
    data=pd.read_excel(excel_path)
    # 确保 SASA 列包含数值
    data['SASA'] = pd.to_numeric(data['SASA'], errors='coerce')

    # 删除 SASA 列中包含 NaN 值的行
    data = data.dropna(subset=['SASA'])

    # # 检查数据中是否有无效值（如负值或过大的值）
    # data = data[(data['SASA'] >= 0) & (data['SASA'] < 1e6)]

    # 进一步检查数据是否包含无效值
    # invalid_values = data[~np.isfinite(data['SASA'])]
    # print(f"Invalid values:\n{invalid_values}")

    # 只保留有效值
    data = data[np.isfinite(data['SASA'])]

    wt2_data = data[data['Object'] == 'wt2']['SASA']
    mt3_data = data[data['Object'] == 'mt3']['SASA']

    # ————————————

    # # 计算WT2的核密度估计
    # kde = sns.kdeplot(wt2_data, bw_adjust=0.5).get_lines()[0].get_data()
    # x_kde, y_kde = kde
    #
    # # 找到峰值和谷值
    # peaks, _ = find_peaks(y_kde)
    # valleys, _ = find_peaks(-y_kde)
    #
    # # 获取峰谷的横坐标
    # peak_positions = x_kde[peaks]
    # valley_positions = x_kde[valleys]
    #
    # # 打印峰谷的位置
    # print(f"峰值位置: {peak_positions}")
    # print(f"谷值位置: {valley_positions}")

    # ————————————

    # 使用 matplotlib 和 seaborn 绘制直方图和核密度估计图
    fig=plt.figure(figsize=(14, 7))
    figs.append(fig)
    # 绘制 WT2 的图
    plt.hist(wt2_data, bins=30, density=True, alpha=0.6, color='blue', label='WT2')
    sns.kdeplot(wt2_data, color='blue', bw_adjust=0.5)

    # sns.kdeplot(wt2_data, color='blue', bw_adjust=0.5)

    # plt.scatter(peak_positions, y_kde[peaks], color='red', zorder=5, label='峰值')
    # plt.scatter(valley_positions, y_kde[valleys], color='green', zorder=5, label='谷值')

    # 绘制 MT3 的图
    plt.hist(mt3_data, bins=30, density=True, alpha=0.6, color='red', label='MT3')
    sns.kdeplot(mt3_data, color='red', bw_adjust=0.5)

    # 添加标签和标题
    plt.xlabel('SASA')
    plt.ylabel('密度')
    plt.title('SASA频率分布图')
    plt.legend()
    plt.savefig(f"{get_filename_without_suffix(excel_path)}.png")

# 显示图表，并在30s后自动关闭
plt.show()
sleep(30)
close_all_fig(figs)













