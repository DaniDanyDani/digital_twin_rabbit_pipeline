import numpy as np

class ECGBase:
    """
    Estrutura de dados pura para o sinal de ECG.
    Sem funções de I/O, apenas estado e lógica matemática.
    """
    def __init__(self):
        self.fs = None                 # Frequência de amostragem (Hz)
        self.signals = None            # Matriz (Amostras x Canais)
        self.electrode_coords = None   # Matriz (Canais x 3) [X, Y, Z]
        self.electrode_ids = None      # Array (Canais,)


class ECGRaw(ECGBase):
    """
    Modelo de dados para o Tanque/Simulação.
    """
    def __init__(self):
        super().__init__()
        self.vertices = None
        self.faces = None
        self.is_processed = False

    def populate_from_arrays(self, vertices, faces, el_map, tank_data_matrix, fs_original: float = 4000.0):
        """Preenche o objeto a partir de arrays puros do NumPy."""
        self.vertices = vertices
        self.faces = faces
        
        # Mapeamento
        self.electrode_ids = el_map[:, 0].astype(int)
        vertex_indices = el_map[:, 1].astype(int) - 1
        self.electrode_coords = self.vertices[vertex_indices]
        
        # Garante o formato (Amostras, Canais)
        if tank_data_matrix.shape[0] == len(self.electrode_ids):
            self.signals = tank_data_matrix.T
        else:
            self.signals = tank_data_matrix
            
        self.fs = fs_original

    def preprocess(self, fs_target: float = 1000.0, time_window: list = [0, 1000], reference_id=None):
        """Lógica de processamento de sinal pura."""
        if self.signals is None:
            raise ValueError("O objeto ECG está vazio.")

        t_ini, t_fim = time_window
        
        # Referência
        if reference_id is not None:
            try:
                ref_idx = np.where(self.electrode_ids == reference_id)[0][0]
                ref_signal = self.signals[:, ref_idx]
                self.signals = self.signals - ref_signal[:, np.newaxis]
            except IndexError:
                print(f"Aviso: Referência {reference_id} não encontrada.")

        # Janela
        start_idx = int(t_ini * (self.fs / 1000.0))
        end_idx = int(t_fim * (self.fs / 1000.0))
        
        # Reamostragem (Stride)
        stride = int(self.fs / fs_target)
        self.signals = self.signals[start_idx:end_idx:stride, :]
        self.fs = fs_target
        self.is_processed = True