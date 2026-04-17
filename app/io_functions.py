import os
import csv
import numpy as np
import pyvista as pv
import scipy.io as sio

# Importamos nossas classes de dados
from app.ecg import ECGBase, ECGRaw

# =====================================================================
# FUNÇÕES DE LEITURA (IN)
# =====================================================================

def read_mat_dict(mat_path, variable_name=None):
    """Lê o arquivo .mat ignorando metadados do MATLAB."""
    if not os.path.exists(mat_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {mat_path}")
    
    mat_contents = sio.loadmat(mat_path)
    
    if variable_name is not None:
        try:
            return mat_contents[variable_name][0, 0]
        except IndexError:
            return mat_contents[variable_name]
            
    return {k: v for k, v in mat_contents.items() if not k.startswith('__')}

def load_ecg_from_mat(mat_path: str, fs_original: float = 4000.0) -> ECGRaw:
    """
    Função Fábrica: Lê o arquivo físico e retorna um objeto ECGRaw preenchido.
    """
    print(f"Lendo dados físicos de: {mat_path}")
    data_struct = read_mat_dict(mat_path, 'data')
    
    geometries = data_struct['geometries'][0, 0]
    signals = data_struct['signal'][0, 0]
    
    vertices = geometries['tank_geo'][0, 0]['vertices']
    faces = geometries['tank_geo'][0, 0]['faces']
    el_map = geometries['el_map']
    tank_data = signals['tank']

    # Instancia o objeto e popula com os arrays puros
    ecg_obj = ECGRaw()
    ecg_obj.populate_from_arrays(vertices, faces, el_map, tank_data, fs_original)
    
    return ecg_obj

# =====================================================================
# FUNÇÕES DE ESCRITA (OUT)
# =====================================================================

def save_ecg_to_csv(ecg_obj: ECGBase, output_dir: str = "./", base_name: str = "tank_data"):
    """Exporta coordenadas e sinais de qualquer objeto que herde de ECGBase para CSV."""
    if ecg_obj.signals is None:
        raise ValueError("O objeto ECG não possui sinais para salvar.")

    os.makedirs(output_dir, exist_ok=True)
    path_coords = os.path.join(output_dir, f"{base_name}_coords.csv")
    path_signals = os.path.join(output_dir, f"{base_name}_signals.csv")

    # Escreve Coordenadas
    with open(path_coords, mode='w', newline='') as f_coords:
        writer = csv.writer(f_coords)
        for el_id, coord in zip(ecg_obj.electrode_ids, ecg_obj.electrode_coords):
            writer.writerow([el_id, coord[0], coord[1], coord[2]])

    # Escreve Sinais (Por linha, transpondo a matriz (Amostras, Canais))
    with open(path_signals, mode='w', newline='') as f_signals:
        writer = csv.writer(f_signals)
        for channel_signal in ecg_obj.signals.T:
            writer.writerow(channel_signal.tolist())

    print(f"CSVs salvos em: {output_dir}")

def export_mesh_to_vtk(ecg_obj: ECGRaw, output_dir: str = "./", output_filename: str = "tank_with_el.vtk"):
    """Exporta malha VTK a partir de um ECGRaw (que possui geometria)."""
    if ecg_obj.vertices is None:
        raise ValueError("Este objeto ECG não possui geometria 3D acoplada.")

    num_faces = ecg_obj.faces.shape[0]
    padding = np.full((num_faces, 1), 3)
    vtk_faces = np.hstack((padding, ecg_obj.faces - 1)).flatten()
    
    mesh = pv.PolyData(ecg_obj.vertices, vtk_faces)
    electrode_labels = np.full(ecg_obj.vertices.shape[0], -1, dtype=int)
    
    for el_id, coord in zip(ecg_obj.electrode_ids, ecg_obj.electrode_coords):
        vertex_idx = np.where((ecg_obj.vertices == coord).all(axis=1))[0][0]
        electrode_labels[vertex_idx] = el_id
        
    mesh.point_data["electrode"] = electrode_labels
    
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, output_filename)
    mesh.save(full_path)
    print(f"VTK salvo: {full_path}")