@echo off
:: 自动安装依赖的批处理脚本

echo 正在安装Numpy（Pymol安装所需文件1/5）……
pip install numpy

echo 正在安装MKL（Pymol所需文件2/5）……
pip install mkl

echo 正在安装PMW（Pymol安装所需文件3/5）……
pip install pmw

echo 正在安装Pymol（Pymol安装所需文件4/5）……
pip install pymol-3.0.0-cp39-cp39-win_amd64.whl

echo 正在安装Pymol的GUI plus版本（Pymol安装所需文件5/5）……
pip install pyqt5

echo 安装完成，20秒后自动关闭窗口
timeout /t 20

:: 关闭CMD窗口
exit
