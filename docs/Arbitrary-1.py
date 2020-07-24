import matplotlib.pyplot as plt
import numpy as np
import rtdpy
#
# Create Square RTD function
def fun(t):
    # Square RTD function between times 10 and 15.
    return 1 / (15 - 10) * np.greater(t, 10) * np.less(t, 15)
rtdmodel = rtdpy.Arbitrary(fun, dt=.01, time_end=20)
plt.plot(rtdmodel.time, rtdmodel.exitage, label="Square RTD")
print(f"Square RTD mean residence time: {rtdmodel.mrt():.1f}")
# Square RTD mean residence time: 12.5
#
# Create a model from experimental data
t_data = np.array([0, 1, 2, 3, 4, 5], dtype=float)
C_data = np.array([0.5, 0.2, 0.3, 0.15, 0.1, 0.0], dtype=float)
def fun_data(t):
    return np.interp(t, t_data, C_data, left=0, right=0)
rtdmodel_data = rtdpy.Arbitrary(fun_data, dt=.01, time_end=20)
#
# Plot arbitrary models
plt.plot(rtdmodel_data.time, rtdmodel_data.exitage, label="Data RTD")
plt.xlabel('Time')
plt.ylabel('Exit Age Function')
plt.legend()
print(f"Data RTD mean residence time: {rtdmodel_data.mrt():.1f}")
# Data RTD mean residence time: 1.7
plt.show()
