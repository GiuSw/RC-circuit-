import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Configurazione della figura e del grafico
fig, ax = plt.subplots(figsize=(7, 6))
plt.subplots_adjust(bottom=0.25)  # Spazio in basso per gli slider

# Limiti del grafico
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.axhline(0, color='black', lw=0.5, ls='--')
ax.axvline(0, color='black', lw=0.5, ls='--')
ax.set_title("Simulazione Conica Degenere: $x^2 + 2kx + c = 0$")
ax.set_xlabel("x")
ax.set_ylabel("y")

# Parametri iniziali (reali e distinte: x^2 - 4 = 0 -> x = ±2)
k_init = 0.0
c_init = -4.0

# Linee verticali che rappresentano le rette della conica
line1 = ax.axvline(x=np.nan, color='blue', lw=2, label='Retta 1')
line2 = ax.axvline(x=np.nan, color='red', lw=2, label='Retta 2')
text_status = ax.text(-4.5, 4, "", fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

def calcola_e_aggiorna(k, c):
    """Calcola le soluzioni di x^2 + 2kx + c = 0 e aggiorna il grafico"""
    delta = (2*k)**2 - 4*c  # Δ = 4k^2 - 4c
    
    if delta > 0:
        # Due rette reali e distinte (Rango B = 2)
        x1 = (-2*k + np.sqrt(delta)) / 2
        x2 = (-2*k - np.sqrt(delta)) / 2
        line1.set_xdata([x1, x1])
        line2.set_xdata([x2, x2])
        line1.set_visible(True)
        line2.set_visible(True)
        text_status.set_text(f"Δ > 0\nRango(B) = 2\nRette Parallele REALI e DISTINTE\nx1 = {x1:.2f}, x2 = {x2:.2f}")
    elif np.isclose(delta, 0, atol=1e-4):
        # Due rette reali e coincidenti (Rango B = 1)
        x_coinc = -2*k / 2
        line1.set_xdata([x_coinc, x_coinc])
        line2.set_visible(False)  # Nascondiamo la seconda perché coincide
        text_status.set_text(f"Δ = 0\nRango(B) = 1\nRette REALI e COINCIDENTI\nx = {x_coinc:.2f}")
    else:
        # Rette immaginarie (Rango B = 2, nessun punto reale)
        line1.set_visible(False)
        line2.set_visible(False)
        text_status.set_text("Δ < 0\nRango(B) = 2\nPUNTI IMMAGINARI\n(Nessuna retta visibile nel piano reale)")
    
    fig.canvas.draw_idle()

# Disegna lo stato iniziale
calcola_e_aggiorna(k_init, c_init)

# Definizione degli assi per gli slider
ax_k = plt.axes([0.15, 0.1, 0.7, 0.03])
ax_c = plt.axes([0.15, 0.05, 0.7, 0.03])

# Creazione degli slider
slider_k = Slider(ax_k, 'Parametro k', -3.0, 3.0, valinit=k_init, valfmt='%1.1f')
slider_c = Slider(ax_c, 'Parametro c', -5.0, 5.0, valinit=c_init, valfmt='%1.1f')

# Funzione di callback per l'aggiornamento dinamico
def update(val):
    k = slider_k.val
    c = slider_c.val
    calcola_e_aggiorna(k, c)

slider_k.on_changed(update)
slider_c.on_changed(update)

ax.legend(loc='upper right')
plt.show()