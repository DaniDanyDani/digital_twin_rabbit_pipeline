import numpy as np
import matplotlib.pyplot as plt

def convert_txt_to_leads_csv(txt_path, csv_path, delimiter=None):
    """
    Converte um arquivo .txt de leituras ECG para um .csv onde:
    - A primeira coluna (tempo) é ignorada
    - Cada linha no CSV é um eletrodo (lead)
    - Cada coluna é um instante de tempo

    Parâmetros:
    - txt_path: caminho para o .txt de entrada
    - csv_path: caminho para salvar o .csv
    - delimiter: separador usado no .txt (padrão: espaço/tab automático)
    """
    try:
        data = np.genfromtxt(txt_path, delimiter=delimiter)
        if data.ndim != 2 or data.shape[1] < 2:
            raise ValueError("Esperado: uma coluna de tempo + pelo menos uma de leitura.")

        leads = data[:, 1:]              # remove a coluna de tempo
        leads = leads.T                  # transpor: cada linha será um eletrodo

        np.savetxt(csv_path, leads, delimiter=',')
        print(f"[✓] Dados salvos em formato (eletrodos x tempo) em: {csv_path}")

    except Exception as e:
        print(f"[X] Erro: {e}")


def plot_electrodes_from_csv(filename, range_eletrodos=(0, 60), duration_ms=1000):
    """
    Plota um intervalo de eletrodos de um CSV.

    Parâmetros:
    - filename: caminho para o arquivo CSV.
    - range_eletrodos: tupla (início, fim) indicando o range de eletrodos a plotar.
    - duration_ms: duração total dos dados no eixo do tempo, em milissegundos.
    """
    data = np.genfromtxt(filename, delimiter=',')

    if data.ndim == 1:
        data = data[np.newaxis, :]  # caso só tenha 1 linha

    start_e, end_e = range_eletrodos
    selected_data = data[start_e:end_e]

    num_electrodes, num_samples = selected_data.shape
    time = np.linspace(0, duration_ms, num_samples)

    plt.figure(figsize=(12, 6))

    for i in range(num_electrodes):
        plt.plot(time, selected_data[i], label=f'Eletrodo {start_e + i}')

    plt.title(f"Eletrodos {start_e} a {end_e - 1} de {filename}")
    plt.xlabel("Tempo (ms)")
    plt.ylabel("Amplitude")
    plt.legend(loc='upper right', ncol=2, fontsize=8)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


import numpy as np
import matplotlib.pyplot as plt

def plot_experimental_and_simulated(exp_csv, sim_csv, range_exp, range_sim, duration_ms=1000, sim_start_ms=1000, sim_end_ms=6000):
    """
    Plota dados experimentais e simulados juntos, normalizando simulado pela amplitude do experimental.
    
    Parâmetros:
    - exp_csv: caminho do csv experimental
    - sim_csv: caminho do csv simulado
    - range_exp: tupla (start, end) dos eletrodos experimentais a plotar (intervalo python-style)
    - range_sim: tupla (start, end) dos eletrodos simulados a plotar (intervalo python-style)
    - duration_ms: duração do sinal experimental em ms (assume tempo de 0 a duration_ms)
    - sim_start_ms: tempo inicial do simulado em ms (default 1000 ms)
    - sim_end_ms: tempo final do simulado em ms (default 6000 ms)
    """

    # Carrega dados
    exp_data_full = np.genfromtxt(exp_csv, delimiter=',')
    sim_data_full = np.genfromtxt(sim_csv, delimiter=',')

    # Seleciona intervalo dos eletrodos
    exp_data = exp_data_full[range_exp[0]:range_exp[1], :]
    sim_data = sim_data_full[range_sim[0]:range_sim[1], :]

    # Vetores de tempo
    time_exp = np.linspace(0, duration_ms, exp_data.shape[1])
    time_sim = np.linspace(sim_start_ms, sim_end_ms, sim_data.shape[1])

    # Normaliza simulado pela amplitude global do experimental
    max_abs_exp = np.abs(exp_data).max()
    max_abs_sim = np.abs(sim_data).max()
    scale_factor = max_abs_exp / max_abs_sim if max_abs_sim != 0 else 1.0
    sim_data_scaled = sim_data * scale_factor

    plt.figure(figsize=(12, 8))

    n_plot = min(exp_data.shape[0], sim_data.shape[0])

    for i in range(n_plot):
        plt.plot(time_exp, exp_data[i], color='blue', alpha=0.6, label='Experimental' if i == 0 else "")
        plt.plot(time_sim, sim_data_scaled[i], color='red', linestyle='--', alpha=0.7, label='Simulado (normalizado)' if i == 0 else "")

    plt.title("ECG Experimental vs Simulado (Simulado ajustado para escala Experimental)")
    plt.xlabel("Tempo (ms)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


tank_input_name = "./Tank.csv"
sim_input_name = "./outputs/coelho_salinet/ecg.txt"
sim_output_name = "./Sim_FE.csv"

print("Plotando tank face FE")
plot_electrodes_from_csv(tank_input_name, range_eletrodos=(45,50), duration_ms=1000)


print("Convertendo txt em csv")
convert_txt_to_leads_csv(sim_input_name, sim_output_name, delimiter=' ')


print("Plotando csv")
plot_electrodes_from_csv(sim_output_name, range_eletrodos=(5,10), duration_ms=1000)

plot_experimental_and_simulated(
    exp_csv="./Tank.csv",
    sim_csv="./Sim_FE.csv",
    range_exp=(45, 50),
    range_sim=(5, 10),
    duration_ms=1000,
    sim_start_ms=30,
    sim_end_ms=1000
)

