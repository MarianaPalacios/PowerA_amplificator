from matplotlib import pyplot as plt
f_min = 100
f_max = 2500
dev_x = [0, f_min, f_max, f_max*1.5]
dev_y = [0, 1, 1, 0]
plt.title("Aproximacion diagrama bode")
plt.ylabel('AV')
plt.xlabel('F')
plt.plot(dev_x,dev_y)
plt.show()