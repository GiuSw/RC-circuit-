import numpy as np
import matplotlib.pyplot as plt

t_ltspice = []
tensions_ltspice = []
current_ltspice = []

t_sperimentale = []
tension_sperimentale = []


# Lettura file
f_ltspice = open("valori_numerici.txt", "r", encoding="utf-8")
f_sperimentale = open("dati_tau_teorico.txt", "r", encoding="utf-8")

f_ltspice.readline()
for line in f_ltspice: 
    line = line.strip()
    values = line.split()
    t_ltspice.append(float(values[0]))
    tensions_ltspice.append(float(values[1]))
    current_ltspice.append(float(values[2]))

for line in f_sperimentale: 
    line = line.strip()
    if line:
        values = line.split( ";")
        # CORREZIONE: divido per 1000 se i dati nel file sono in ms
        t_sperimentale.append(float(values[0]) / 1000) 
        tension_sperimentale.append(float(values[1]))

f_ltspice.close()
f_sperimentale.close()



# Conversione in array
t_ltspice = np.array(t_ltspice)
tensions_ltspice = np.array(tensions_ltspice)
current_ltspice = np.array(current_ltspice)

t_sperimentale = np.array(t_sperimentale)
tension_sperimentale = np.array(tension_sperimentale)


C = 100e-6 
R = 10000.0 
E = 5
tau_teorico = R*C


current_teorica = (E / R) * np.exp(-t_sperimentale/ tau_teorico)


t_quinto = t_ltspice[:len(t_ltspice)//5]
m = 5 / (R * C) 
y = m * t_quinto


#Interpolazione lineare
log_ltspice = np.log(E - tensions_ltspice)
log_interp = np.interp(t_sperimentale, t_ltspice, log_ltspice)
v_spice_interp_esponenziale = E - np.exp(log_interp)

errore_punto_punto = tension_sperimentale - v_spice_interp_esponenziale

sottomultipli = np.arange(-1, 5.1, 0.5)


# GRAFICO 1 (Tensione e Corrente - Tau Teorica)
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.suptitle(f"Evoluzione Circuito RC (Tau Teorica = {tau_teorico})")
plt.plot(t_ltspice, tensions_ltspice, color="blue", label="Tensione Numerica", linestyle = "--")
plt.plot(t_quinto, y, color="red", label="Tangente") 
plt.plot(t_sperimentale, tension_sperimentale, color="green", label="Tensione Misurata", linewidth = 2)
plt.ylabel("Volt (V)")
plt.xticks(sottomultipli)
plt.xlim(0, 5) 
plt.legend()
plt.grid(True)  

plt.subplot(2, 1, 2)
plt.plot(t_sperimentale, current_teorica, color="red", label="Corrente Calcolata", linewidth = 2)
plt.plot(t_ltspice, current_ltspice, color="blue", label="Corrente Numerica", linestyle = "--")
plt.xlabel("Tempo (s)")
plt.ylabel("Ampere (A)")
plt.xlim(-1, 5) 
plt.xticks(sottomultipli)
plt.legend()
plt.grid(True)

plt.figure(figsize=(10, 5))

plt.plot(t_sperimentale, errore_punto_punto, color="red", marker="o", linestyle="-", linewidth = 1, label="Errore ($V_{arduino} - V_{spice}$)")
plt.axhline(0, color="black", linestyle="--", linewidth=1)
sottomultipli = np.arange(0, 5.1, 0.5)
plt.xticks(sottomultipli)
plt.xlim(0, 5)
plt.title("Andamento dell'Errore di Tensione Punto per Punto")
plt.xlabel("Tempo (s)")
plt.ylabel("Differenza di Tensione (Volt)") 
plt.grid(True)
plt.legend()

plt.show()