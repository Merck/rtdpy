a = rtdpy.Ncstr(tau=10, n=2, dt=.01, time_end=200)
times = np.linspace(1, 60, 10)
disturbances = np.linspace(-100, 100, 10)
x, y, response = a.funnelplot(times, disturbances)

cs = plt.contour(x, y, response)
plt.clabel(cs, fmt='%1.0f')
plt.xlabel('Time of Disturbance')
plt.ylabel('Magnitude of Disturbance')