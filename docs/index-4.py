a = rtdpy.Ncstr(tau=10, n=1, dt=1, time_end=100)

signal_time = np.arange(0, 100, 1)
input_signal = np.zeros(signal_time.size)
input_signal[10:30] = 1
output_signal = a.output(signal_time, input_signal)

# predicted output_signal is longer than input_signal
plt.plot(signal_time, input_signal, label='Input Signal')
plt.plot(signal_time, output_signal[:signal_time.size],
         label='Output Signal')
plt.xlabel('Time')
plt.legend()