import matplotlib.pyplot as plt
import rtdpy
a = rtdpy.Convection(tau=1, dt=.01, time_end=2)
plt.plot(a.time, a.exitage, label='E')
plt.plot(a.time, a.exitage_star, label='E*')
plt.plot(a.time, a.exitage_star2, label='E**')
plt.xlabel('Time')
plt.ylabel('Exit Age Function')
plt.legend()
plt.show()
