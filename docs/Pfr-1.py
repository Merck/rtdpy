import matplotlib.pyplot as plt
import rtdpy
a = rtdpy.Pfr(tau=1, dt=.01, time_end=3)
plt.plot(a.time, a.exitage)
plt.xlabel('Time')
plt.ylabel('Exit Age Function')
plt.show()
