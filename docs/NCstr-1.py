import matplotlib.pyplot as plt
import rtdpy
for n in [1, 2, 10]:
    a = rtdpy.Ncstr(tau=1, n=n, dt=.01, time_end=3)
    plt.plot(a.time, a.exitage, label=f"n={n}")
plt.xlabel('Time')
plt.ylabel('Exit Age Function')
plt.legend()
plt.show()
