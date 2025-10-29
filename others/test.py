import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x**2 + 1


a = 0   
b = 2   
n = 4   


h = (b - a) / n


x = np.linspace(a, b, n + 1)
y = f(x)


I_trap = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])


I_exact = (b**3 / 3 + b) - (a**3 / 3 + a)


error_abs = abs(I_exact - I_trap)
error_rel = (error_abs / I_exact) * 100


print("=== Metode Trapezoidal untuk f(x)=x^2+1 ===")
print(f"Hasil Trapezoidal  = {I_trap:.6f}")
print(f"Nilai Eksak        = {I_exact:.6f}")
print(f"Error Absolut      = {error_abs:.6f}")
print(f"Error Relatif (%)  = {error_rel:.3f}%")


x_plot = np.linspace(a, b, 100)
y_plot = f(x_plot)

plt.figure(figsize=(8, 5))
plt.plot(x_plot, y_plot, 'b', label='f(x) = x² + 1')


for i in range(n):
    x_trap = [x[i], x[i], x[i+1], x[i+1]]
    y_trap = [0, f(x[i]), f(x[i+1]), 0]
    plt.fill(x_trap, y_trap, 'orange', alpha=0.3, edgecolor='red')

plt.scatter(x, y, color='red')

plt.title("Visualisasi Metode Trapezoidal untuk f(x)=x²+1")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()
