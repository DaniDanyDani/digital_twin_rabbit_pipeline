import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def resample_csv(input_csv, output_csv=None, duration_ms=1000):
    data = np.genfromtxt(input_csv, delimiter=',')
    print(f"Shape dos dados de {input_csv}: {data.shape}")
    print(data)

    num_electrodes, original_samples = data.shape

    # Eixo de tempo original e novo (em ms)
    original_time = np.linspace(0, duration_ms, original_samples)
    target_time = np.linspace(0, duration_ms, 1000)  # 1 ms por coluna

    resampled_data = np.zeros((num_electrodes, 1000))

    for i in range(num_electrodes):
        interp_func = interp1d(original_time, data[i], kind='linear')
        resampled_data[i] = interp_func(target_time)

    if output_csv:
        np.savetxt(output_csv, resampled_data, delimiter=',')

    return resampled_data

def resample_ecg_txt(input_file, output_csv=None, start_ms=1000, end_ms=2000):
    data = np.genfromtxt(input_file)
    timesteps = data[:, 0]  # tempo (em ms ou s)
    currents = data[:, 1:]  # cada coluna = 1 eletrodo

    if timesteps[-1] <= 10:  # converte para ms se estiver em segundos
        timesteps = timesteps * 1000

    num_samples, num_leads = currents.shape

    duration_ms = end_ms - start_ms
    # Cria vetor de tempo entre start_ms e end_ms com 1000 pontos (1 ms passo)
    target_time = np.linspace(start_ms, end_ms, 1000)

    resampled_data = np.zeros((num_leads, 1000))  # linhas = eletrodos, colunas = tempo

    for i in range(num_leads):
        interp_func = interp1d(timesteps, currents[:, i], kind='linear', fill_value="extrapolate")
        resampled_data[i] = interp_func(target_time)

    if output_csv:
        np.savetxt(output_csv, resampled_data, delimiter=',')
        print(f"[✓] ECG simulado reamostrado salvo em: {output_csv}")

    return resampled_data


import numpy as np
import matplotlib.pyplot as plt

def plot_experiment_vs_simulation(experimental, simulated, duration_ms=1000):
    num_electrodes_exp, num_samples_exp = experimental.shape
    num_electrodes_sim, num_samples_sim = simulated.shape

    assert num_electrodes_exp == num_electrodes_sim, "Nº de eletrodos incompatível entre experimental e simulado"

	# Normaliza simulado entre os extremos absolutos do experimental
	max_exp = np.abs(exp_data).max()
	min_exp = np.abs(exp_data).min()
	amplitude_exp = max_exp - min_exp

	max_sim = np.abs(sim_data).max()
	min_sim = np.abs(sim_data).min()
	amplitude_sim = max_sim - min_sim

	scale_factor = amplitude_exp / amplitude_sim if amplitude_sim != 0 else 1.0
	sim_data_scaled = sim_data * scale_factor


    plt.figure(figsize=(12, 8))

    for i in range(num_electrodes_exp):
        if i >=0:
            #plt.plot(time_exp, experimental[i], color='blue', alpha=0.6, label='Experimental' if i == 0 else "")
            plt.plot(time_exp, simulated_norm[i], color='red', linestyle='--', alpha=0.7, label='Simulado Normalizado' if i == 0 else "")

    plt.title("ECG Experimental vs Simulado (Simulado ajustado para escala Experimental)")
    plt.xlabel("Tempo (ms)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def main():

	tank_csv = "./Tank.csv"
	csv_resampled_name = "./Tank_resampled.csv"
	experimental_resampled = resample_csv(tank_csv, csv_resampled_name, duration_ms = 1000)

	input_file = "./outputs/coelho_salinet/ecg.txt"
	input_resampled_name = "./ecg_resampled.csv"
	simulation_resampled = resample_ecg_txt(input_file, input_resampled_name, start_ms=1000, end_ms=2000)
	
	experimental_resampled = np.genfromtxt("Tank_resampled.csv", delimiter=',')[10:20]
	simulation_resampled = np.genfromtxt("ecg_resampled.csv", delimiter=',')
	
	plot_experiment_vs_simulation(experimental_resampled, simulation_resampled)


if __name__ == "__main__":
	main()
