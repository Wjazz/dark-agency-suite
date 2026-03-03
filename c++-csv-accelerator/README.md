# C++ CSV Accelerator for Python (Pybind11) 🚀

Un micro-módulo de alto rendimiento diseñado para acelerar la ingesta y parseo de grandes volúmenes de datos tabulares (CSV), resolviendo el cuello de botella tradicional de I/O en pipelines de Python puro.

## 🎯 El Problema que Resuelvo
En entornos de *People Analytics* e Infraestructura de Datos, la lectura y transformación de archivos masivos utilizando librerías estándar (`pandas.read_csv`) bloquea el hilo principal (GIL) y consume exceso de memoria RAM.

## 🛠️ La Solución Arquitectónica
He implementado un *parser* numérico eficiente escrito enteramente en **C++17** (utilizando contigüidad de memoria y prevención de copias innecesarias) y lo he expuesto nativamente a Python utilizando **Pybind11**. 

Esto permite:
1. **Bypasear el overhead** del intérprete de Python durante la lectura en disco.
2. Integrarse limpiamente en arquitecturas de ETL existentes sin fricción.

## 📊 Benchmark Real (Demostración)
Para un archivo de prueba simulado de 200,000 registros numéricos:
* *Pandas Read Time:* ~ `X` segundos
* *C++ Accelerator Time:* ~ `Y` segundos
* **Aceleración Total (Ratio):** `Z`x más rápido.

## ⚙️ Reproducción en 1 Clic
Este módulo está completamente Dockerizado para asegurar una compilación limpia y repetible en cualquier sistema (sin ensuciar el *host* con dependencias de C++).

Ejecuta el siguiente script en tu terminal para compilar el módulo y lanzar el benchmark automáticamente:

```bash
./demo.sh
