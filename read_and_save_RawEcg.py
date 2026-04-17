from app.io_functions import load_ecg_from_mat, save_ecg_to_csv, export_mesh_to_vtk

# 1. I/O: Lê do disco
meu_ecg = load_ecg_from_mat('data/input/raw/data-sinus.mat')

# 2. Lógica: Processa em memória RAM
meu_ecg.preprocess(fs_target=1000, time_window=[40, 120])

# 3. I/O: Salva no disco
save_ecg_to_csv(meu_ecg, output_dir='data/output/pre_process_raw', base_name='coelho_1000hz_40-120ms')
export_mesh_to_vtk(meu_ecg, output_dir='data/output/mesh')