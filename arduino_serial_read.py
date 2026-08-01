import serial 
import time 
import numpy as np
import matplotlib.pyplot as plt

arduino = serial.Serial('COM5', 9600)
time.sleep(2) 

f_tau_teorico = open("dati_tau_teorico.txt", "w", encoding="utf-8")

t = []
tension = []
transitorio = True
C = 100e-6 
R = 10000.0 
E = 5.0 
tau_teorico = R * C 

# --- Acquisizione Dati ---
print("Acquisizione in corso... Inserisci il GND")
while(transitorio):
    line = arduino.readline().decode('ascii', errors='replace').strip()
    
    if "TRANSITORIO_CONCLUSO" in line:
        transitorio = False
        print("Ricevuto segnale di fine transitorio.")
        
    elif ";" in line: 
        f_tau_teorico.write(line + "\n")
        values = line.split(";")
        t.append(float(values[0]))
        tension.append(float(values[1]))

arduino.close()
f_tau_teorico.close()   

# --- Elaborazione Dati ---
t_array = np.array(t) / 1000.0 
tension_array = np.array(tension)


#Definizione segmenti per le tangenti (primo 20% della durata)
t_quinto = t_array[:len(t_array) // 5]

m = E / tau_teorico
y_retta_tan = m * t_quinto

#Calcolo Correnti
corrente_teorica = (E / R) * np.exp(-t_array / tau_teorico)

plt.figure(figsize=(10, 8))
plt.suptitle('EVOLUZIONE CIRCUITO RC')

plt.subplot(2, 1, 1)
plt.plot(t_array, tension_array, color='blue', label='V Sperimentale') 
plt.axhline(y=E, color='green', label='Asintoto E (5V)') 
plt.plot(t_quinto, y_retta_tan, 'r--', label=f'Tangente Teorica (τ={tau_teorico:.3f}s)')
plt.ylabel('Tensione [V]')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t_array, corrente_teorica, color='red', label='I Teorica (Calcolata)')
plt.ylabel('Corrente [A]')
plt.xlabel('Tempo [s]')
plt.legend()
plt.grid(True)

plt.show()
