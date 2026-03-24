import matplotlib.pyplot as plt
import numpy as np

# 设定时钟周期和仿真的时钟周期数
clk_periods = 5
t = np.arange(0, clk_periods + 0.5, 0.5)

# 生成CLK波形
clk = np.tile([0, 1], clk_periods)

# 绘制时钟波形
plt.figure(figsize=(10, 8))

# CLK waveform
plt.subplot(6, 1, 1)
plt.step(t, clk, 'k-', where='post')
plt.ylim(-0.5, 1.5)
plt.ylabel('CLK')
plt.grid(True)
plt.xticks([])  # 隐藏X轴刻度

# 函数来生成T和D触发器的输出
def flipflop_t_d(clk, t, flipflop_type='T'):
    q = 0
    output_waveform = [q]

    for i in range(1, len(clk)):
        if clk[i-1] == 0 and clk[i] == 1:  # 上升沿
            if flipflop_type == 'T':
                q = not q  # T触发器在每个上升沿切换状态
            else:
                q = 1  # D触发器在上升沿设置Q为D，这里假设D=1
        output_waveform.append(q)

    return np.array(output_waveform)

# 函数来生成JK触发器的输出
def flipflop_jk(clk, t, edge_type='positive'):
    j, k = 1, 1  # 假设J和K始终为1
    q = 0
    output_waveform = [q]

    for i in range(1, len(clk)):
        if (clk[i-1] == 0 and clk[i] == 1 and edge_type == 'positive') or \
           (clk[i-1] == 1 and clk[i] == 0 and edge_type == 'negative'):
            if j == 1 and k == 0:
                q = 1
            elif j == 0 and k == 1:
                q = 0
            elif j == 1 and k == 1:
                q = not q
        output_waveform.append(q)

    return np.array(output_waveform)

# 生成并绘制JK触发器（正边沿）Q1, Q5波形
q1 = flipflop_jk(clk, t, 'positive')
plt.subplot(6, 1, 2)
plt.step(t, q1, 'b-', where='post')
plt.ylim(-0.5, 1.5)
plt.ylabel('Q1, Q5')
plt.grid(True)
plt.xticks([])

# 生成并绘制JK触发器（负边沿）Q2, Q6波形
q2 = flipflop_jk(clk, t, 'negative')
plt.subplot(6, 1, 3)
plt.step(t, q2, 'r-', where='post')
plt.ylim(-0.5, 1.5)
plt.ylabel('Q2, Q6')
plt.grid(True)
plt.xticks([])

# 生成并绘制D触发器 Q3, Q7, Q11波形
qd = flipflop_t_d(clk, t, 'D')
plt.subplot(6, 1, 4)
plt.step(t, qd, 'g-', where='post')
plt.ylim(-0.5, 1.5)
plt.ylabel('Q3, Q7, Q11')
plt.grid(True)
plt.xticks([])

# 生成并绘制T触发器 Q4, Q12波形
qt = flipflop_t_d(clk, t)
plt.subplot(6, 1, 5)
plt.step(t, qt, 'm-', where='post')
plt.ylim(-0.5, 1.5)
plt.ylabel('Q4, Q12')
plt.grid(True)
plt.xticks([])

# 绘制SR触发器 Q8波形 (S=1, R=0)
q8 = np.ones_like(clk)
plt.subplot(6, 1, 6)
plt.step(t, q8, 'c-', where='post')
plt.ylim(-0.5, 1.5)
plt.ylabel('Q8')
plt.xlabel('时间 (t)')
plt.grid(True)

# 显示所有波形图
plt.tight_layout()
plt.show()
