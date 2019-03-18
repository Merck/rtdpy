import matplotlib.pyplot as plt
import rtdpy
for c in [3, 7]:
    a = rtdpy.Zusatz(b=25, c=c, dt=.01, time_end=100)
    plt.plot(a.time, a.exitage, label=f"c={c}")
plt.xlabel('Time')
plt.ylabel('Exit Age Function')
plt.legend()
plt.show()
