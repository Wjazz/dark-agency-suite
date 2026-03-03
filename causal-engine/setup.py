"""
setup.py — Compilación del módulo C++ fast_math con pybind11
=============================================================

Uso:
    pip install pybind11
    python setup.py build_ext --inplace

    # El .so resultante se puede importar directamente:
    #   import fast_math
    #   fast_math.variance([1.0, 2.0, 3.0])
"""

from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

__version__ = "1.0.0"

ext_modules = [
    Pybind11Extension(
        "fast_math",
        sources=["app/core/fast_math.cpp"],
        define_macros=[("VERSION_INFO", __version__)],
        cxx_std=17,
        extra_compile_args=[
            "-O3",           # Optimización agresiva
            "-march=native", # Optimizar para CPU local (quitar para Docker multi-arch)
            "-ffast-math",   # Optimización FP (aceptable para nuestro caso de uso)
            "-Wall",
            "-Wextra",
        ],
    ),
]

setup(
    name="bourbaki-fast-math",
    version=__version__,
    author="Bourbaki Engine Team",
    author_email="james.alvarado@email.com",
    description="Módulo C++ de alto rendimiento para inferencia causal y Bayesiana",
    long_description="",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pybind11>=2.11.0",
    ],
    zip_safe=False,
)
