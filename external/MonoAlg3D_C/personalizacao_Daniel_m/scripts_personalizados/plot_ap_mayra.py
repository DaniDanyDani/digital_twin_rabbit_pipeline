import sys
import numpy as np
import matplotlib.pyplot as plt

def plot_action_potential(ap_file):
    """
    Lê um arquivo de duas colunas e plota a segunda coluna (AP) 
    em função da primeira (tempo).

    Args:
        ap_file (str): O caminho para o arquivo de entrada.
    """
    try:
        # Carrega os dados do arquivo de texto.
        # O numpy identifica automaticamente o separador (espaços).
        print(f"Lendo dados de '{ap_file}'...")
        data = np.genfromtxt(ap_file)

        # A primeira coluna (índice 0) é o tempo.
        # A segunda coluna (índice 1) é o valor do potencial de ação.
        time = data[:, 0]
        ap_value = data[:, 1]

        print(f"Arquivo lido com sucesso. Encontrados {len(time)} pontos de dados.")

        # Cria a figura e o gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(time, ap_value, label="Potencial de Ação", color="blue", linewidth=2)

        # Adiciona títulos e rótulos para maior clareza
        plt.title("Potencial de Ação (AP)", fontsize=16)
        plt.xlabel("Tempo (ms)", fontsize=12)
        plt.ylabel("Potencial de Membrana (mV)", fontsize=12)
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.legend()
        plt.tight_layout()

        # Exibe o gráfico
        plt.show()

    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        print("Verifique se o arquivo está no formato correto (duas colunas de números).")

def main():
    """
    Função principal para executar o script a partir da linha de comando.
    """
    if len(sys.argv) != 2:
        print("---------------------------------------------------------")
        print(f"Uso: python {sys.argv[0]} <arquivo_ap.txt>")
        print("---------------------------------------------------------")
        return 1

    ap_file = sys.argv[1]
    plot_action_potential(ap_file)
    return 0

if __name__ == "__main__":
    main()
