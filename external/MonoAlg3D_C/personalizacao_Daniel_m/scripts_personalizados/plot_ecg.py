import sys
import numpy as np
import matplotlib.pyplot as plt

def read_ecg_readings (input_file):
	data = np.genfromtxt(input_file)
	nlin, ncol = np.shape(data)
	timesteps = data[:,0]
	currents = data[:,1:]
	num_leads = ncol-1
	
	return currents, num_leads, nlin
	
def read_ecg_reference(input_file):
	data = np.genfromtxt(input_file, delimiter=',').T
	nlin, ncol = np.shape(data)
	return data[:,26:36], nlin
def plot_ecg_readings (t_sim, t_ref, simulation_data, reference_data, nleads):
	plt.grid()
	for i in range(nleads):
		if i >=5:
			plt.plot(t_sim, simulation_data[:,i], c="red", linewidth=3.0)
			plt.plot(t_ref, reference_data[:,i], c="blue", linewidth=3.0)
	plt.xlabel("t (ms)",fontsize=15)
	plt.ylabel("Current (mA)",fontsize=15)
	plt.title("ECG reading",fontsize=14)
	plt.legend(loc=0,fontsize=14)
	plt.xlim(0,600)
	plt.show()
		#plt.savefig("ecg_lead_%d.pdf" % (i))

def normalize_simulation_data(simulation_data, reference_data):
    """
    Normaliza os dados da simulação para a faixa de valores (mín/máx) da referência.
    """
    min_ref = np.min(np.abs(reference_data))
    max_ref = np.max(np.abs(reference_data))
    
    min_sim = np.min(np.abs(simulation_data))
    max_sim = np.max(np.abs(simulation_data))
    
    # Aplica a fórmula de normalização para mapear a escala da simulação para a escala da referência
    normalized_data = (simulation_data - min_sim) / (max_sim - min_sim) * (max_ref - min_ref) + min_ref
    
    print(f"Dados da simulação normalizados para o intervalo da referência: [{min_ref:.4f}, {max_ref:.4f}]")
    return normalized_data

def main():
	
	if len(sys.argv) != 3:
		print("-------------------------------------------------------------------------")
		print("Usage:> python %s <input_file>" % sys.argv[0])
		print("-------------------------------------------------------------------------")
		print("<input_file> = Input file with the ECG reading from each timestep")
		print("-------------------------------------------------------------------------")
		return 1

	input_simulation = sys.argv[1]
	input_reference = sys.argv[2]

	simulation_data, num_leads, nlin_sim = read_ecg_readings(input_simulation)
	reference_data, nlin_ref = read_ecg_reference(input_reference)
	t_sim = np.linspace(30, 1000, nlin_sim)
	t_ref = np.linspace(0, 1000, nlin_ref)

	simulation_data_normalized = normalize_simulation_data(simulation_data, reference_data)

	plot_ecg_readings(t_sim, t_ref,simulation_data_normalized, reference_data, num_leads)

if __name__ == "__main__":
	main()
