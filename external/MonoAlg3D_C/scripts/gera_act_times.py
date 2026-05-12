import re

def processar_arquivo(arquivo1):

    # =========================
    # Leitura
    # =========================
    with open(arquivo1, 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines if line.strip()]

    # =========================
    # Filtrar linhas válidas
    # =========================
    linhas_validas = []

    for line in lines:

        colchetes = re.findall(r'\[(.*?)\]', line)

        if len(colchetes) < 1:
            continue

        try:
            # cx,cy,cz,dx,dy,dz
            valores_antes = [float(v) for v in line.split()[0].split(',')]

            # apenas TA (primeiro colchete)
            valores_ta = [float(v) for v in colchetes[0].split()]
        except:
            continue

        if len(valores_antes) == 6 and len(valores_ta) > 0:
            linhas_validas.append(line)

    l = len(linhas_validas)
    print("Número de células:", l)

    if l == 0:
        print("Nenhuma linha válida encontrada.")
        return

    # =========================
    # Número de estímulos (TA)
    # =========================
    colchetes = re.findall(r'\[(.*?)\]', linhas_validas[0])
    valores_ta = colchetes[0].split()
    n_estimulos = len(valores_ta)

    print("Número de estímulos (TA):", n_estimulos)

    # =========================
    # Loop nos estímulos
    # =========================
    for a in range(n_estimulos):

        print(f"Gerando VTK para estímulo {a}")

        with open(f"arquivoVTK_{a:03d}.vtk", "w") as arquivoVTK:

            # =========================
            # Cabeçalho
            # =========================
            arquivoVTK.write("# vtk DataFile Version 3.0\n")
            arquivoVTK.write("vtk output\n")
            arquivoVTK.write("ASCII\n")
            arquivoVTK.write("DATASET UNSTRUCTURED_GRID\n")

            # =========================
            # PONTOS
            # =========================
            arquivoVTK.write(f"POINTS {l*8} float\n")

            for linha in linhas_validas:

                valores_antes = [float(v) for v in linha.split()[0].split(',')]
                cx, cy, cz, dx, dy, dz = valores_antes

                pontos = [
                    (cx - dx, cy - dy, cz - dz),
                    (cx + dx, cy - dy, cz - dz),
                    (cx + dx, cy + dy, cz - dz),
                    (cx - dx, cy + dy, cz - dz),
                    (cx - dx, cy - dy, cz + dz),
                    (cx + dx, cy - dy, cz + dz),
                    (cx + dx, cy + dy, cz + dz),
                    (cx - dx, cy + dy, cz + dz),
                ]

                for p in pontos:
                    arquivoVTK.write(f"{p[0]} {p[1]} {p[2]}\n")

            # =========================
            # CÉLULAS
            # =========================
            arquivoVTK.write(f"CELLS {l} {l*9}\n")

            id_cell = 0
            for _ in linhas_validas:
                arquivoVTK.write(
                    f"8 {id_cell} {id_cell+1} {id_cell+2} {id_cell+3} "
                    f"{id_cell+4} {id_cell+5} {id_cell+6} {id_cell+7}\n"
                )
                id_cell += 8

            # =========================
            # TIPOS
            # =========================
            arquivoVTK.write(f"CELL_TYPES {l}\n")
            for _ in linhas_validas:
                arquivoVTK.write("12\n")  # hexaedro

            # =========================
            # DADOS (TA)
            # =========================
            arquivoVTK.write(f"CELL_DATA {l}\n")
            arquivoVTK.write("SCALARS Activation_Times float 1\n")
            arquivoVTK.write("LOOKUP_TABLE default\n")

            for linha in linhas_validas:

                colchetes = re.findall(r'\[(.*?)\]', linha)

                try:
                    valores = [float(v) for v in colchetes[0].split()]  # só TA
                except:
                    valores = []

                if len(valores) > a:
                    arquivoVTK.write(f"{valores[a]}\n")
                else:
                    arquivoVTK.write("0\n")


# =========================
# EXECUÇÃO
# =========================
processar_arquivo('./outputs/Curvatura/activation_info_it_0.acm')