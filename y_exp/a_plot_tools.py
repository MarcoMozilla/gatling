import platform

import matplotlib.pyplot as plt
import matplotlib
system = platform.system()
if system == "Windows":
    matplotlib.use('TkAgg')  # 有图形界面，使用 TkAgg

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['axes.unicode_minus'] = False
plt.style.use('Solarize_Light2')

plt_show = lambda: plt.show(block=True)