for n in [1, 2, 5, 10, 100]:
    a = rtdpy.Ncstr(tau=1, n=n, dt=.001, time_end=3)
    plt.plot(a.time, a.stepresponse, label=f"n={n}")

plt.xlabel('Time')
plt.ylabel('Exit Age Function')
plt.title('Step Response')
plt.legend()