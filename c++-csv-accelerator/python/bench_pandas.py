import time, csv, os
import sys
# Añadimos la carpeta 'build' (donde se compiló el .so) al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../build')))

import pandas as pd
import csv_accel

def gen_csv(path, nrows=200000, ncols=5):
    import random
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow([f"c{i}" for i in range(ncols)])
        for _ in range(nrows):
            w.writerow([random.random()*100 for _ in range(ncols)])

def bench(path):
    print("--- INICIANDO BENCHMARK ---")
    t0 = time.time()
    df = pd.read_csv(path)
    ptime = time.time() - t0

    t0 = time.time()
    col = csv_accel.read_col_as_list(path, 2)
    ctime = time.time() - t0

    print(f"Pandas Read Time: {ptime:.4f}s")
    print(f"C++ Accelerator Time: {ctime:.4f}s")
    print(f"Ratio: C++ es {ptime/ctime:.2f}x más rápido")

if __name__ == "__main__":
    path = "test.csv"
    if not os.path.exists(path):
        print("Generando CSV de prueba...")
        gen_csv(path)
    bench(path)
