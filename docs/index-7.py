from scipy import optimize

# Generate noisy data from NCSTR system with tau=10 and n=2
a = rtdpy.Ncstr(tau=10, n=2, dt=1, time_end=50)
xdata = a.time
noisefactor = 0.01
ydata = a.exitage \
    + (noisefactor * (np.random.rand(a.time.size) - 0.5))

def f(xdata, tau, n):
    a = rtdpy.Ncstr(tau=tau, n=n, dt=1, time_end=50)
    return a.exitage

# Give initial guess of tau=5 and n=4
popt, pcov = optimize.curve_fit(f, xdata, ydata, p0=[5, 4],
                                bounds=(0, np.inf))
plt.plot(xdata, ydata, label='Impulse Experiment')
b = rtdpy.Ncstr(tau=popt[0], n=popt[1], dt=1, time_end=50)
plt.plot(xdata, b.exitage, label='RTD Fit')
plt.title(f'tau={popt[0]: .2f}, n={popt[1]: .2f}')
plt.legend()