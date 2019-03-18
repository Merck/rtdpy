a = rtdpy.Ncstr(tau=1, n=2, dt=.001, time_end=10)
b = rtdpy.Pfr(tau=3, dt=.001, time_end=10)
c = rtdpy.Elist([a, b])

plt.plot(c.time, c.exitage)
plt.xlabel('Time')
plt.ylabel('Exit Age Function')
plt.title('Combined RTD Model')