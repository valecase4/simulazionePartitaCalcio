import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-50, 50,1000)
y = x+50

plt.figure(figsize=(8, 5))
plt.scatter(0, 50, color='red', zorder=3)
plt.scatter(30, 80, color='red', zorder=3)
plt.scatter(-30, 20, color='red', zorder=3)
plt.plot(x, y, label="y = x+50", color="blue", zorder=2)
plt.axhline(0, color='black', linewidth=1)  # Asse X
plt.axvline(0, color='black', linewidth=1)  # Asse Y
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.title("Grafico della funzione y = x+50")
plt.xlabel("x")
plt.ylabel("y")

plt.xticks([-50,-40,-30,-20,-10,0,10,20,30,40,50])
plt.yticks([0,10,20,30,40,50,60,70,80,90,100])

plt.show()