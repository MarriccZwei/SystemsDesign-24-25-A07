import matplotlib.pyplot as plt
import numpy as np

xs = np.linspace(0, 60, 60)
ys1 = (-1*10**-5)*xs**3 + 0.004*xs**2 - 0.0006*xs + 1.781
ys2 = (3*10**-6)*xs**3 + 0.0009*xs**2 + 0.1023*xs - 0.0857
ys3 = (-6*10**-6)*xs**3 + 0.0014*xs**2 + 0.0303*xs + 1.1905
ys4 = (-1*10**-5)*xs**3 + 0.0018*xs**2 -0.0399*xs + 2.2095

plt.plot(xs, ys1, label='dy 1.2')
plt.plot(xs, ys2, label='dy 2')
plt.plot(xs, ys3, label='dy 3')
plt.plot(xs, ys4, label='dy 4')
plt.legend()
plt.show()