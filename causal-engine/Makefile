# =============================================================================
# Makefile — Bourbaki Causal Engine: Compilación fast_math C++/pybind11
# =============================================================================

.PHONY: build clean test install-deps all

PYTHON ?= python3
PIP    ?= pip3

# --- Targets principales ---

all: install-deps build test

install-deps:
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║  Instalando dependencias de compilación (pybind11)  ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	$(PIP) install pybind11>=2.11.0

build: install-deps
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║  Compilando fast_math.cpp → fast_math.so            ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	$(PYTHON) setup.py build_ext --inplace
	@echo ""
	@echo "✅ Compilación exitosa. Archivo generado:"
	@ls -la fast_math*.so 2>/dev/null || echo "   (buscar en subdirectorios)"
	@echo ""

test: build
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║  Ejecutando tests de validación                      ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	$(PYTHON) -c "\
import fast_math; \
print('=== fast_math module loaded ==='); \
print(f'Version: {fast_math.__version__}'); \
print(); \
print('--- Variance (Welford) ---'); \
v = fast_math.variance([1.0, 2.0, 3.0, 4.0, 5.0]); \
print(f'variance([1,2,3,4,5]) = {v}'); \
assert abs(v - 2.0) < 1e-10, f'Expected 2.0, got {v}'; \
print('  ✅ PASS'); \
print(); \
print('--- Sample Variance (Bessel) ---'); \
sv = fast_math.sample_variance([1.0, 2.0, 3.0, 4.0, 5.0]); \
print(f'sample_variance([1,2,3,4,5]) = {sv}'); \
assert abs(sv - 2.5) < 1e-10, f'Expected 2.5, got {sv}'; \
print('  ✅ PASS'); \
print(); \
print('--- Std Deviation ---'); \
sd = fast_math.std_deviation([1.0, 2.0, 3.0, 4.0, 5.0]); \
print(f'std_deviation([1,2,3,4,5]) = {sd:.6f}'); \
assert abs(sd - 1.414214) < 1e-4, f'Expected ~1.414, got {sd}'; \
print('  ✅ PASS'); \
print(); \
print('--- Bayesian Normal Posterior ---'); \
mu, sigma = fast_math.bayesian_normal_posterior(0.0, 1.0, [1.0, 2.0, 3.0], 1.0); \
print(f'posterior(prior=N(0,1), data=[1,2,3], σ=1) → N({mu:.4f}, {sigma:.4f})'); \
print('  ✅ PASS'); \
print(); \
print('--- Bayesian Beta Posterior ---'); \
a, b, mean, var = fast_math.bayesian_beta_posterior(1.0, 1.0, 7, 10); \
print(f'posterior(Beta(1,1), 7/10) → Beta({a:.1f}, {b:.1f}), mean={mean:.4f}'); \
assert abs(mean - 8.0/12.0) < 1e-4, f'Expected ~0.6667, got {mean}'; \
print('  ✅ PASS'); \
print(); \
print('═══════════════════════════════════════════'); \
print('  🎯 ALL TESTS PASSED — fast_math is ready'); \
print('═══════════════════════════════════════════'); \
"

clean:
	@echo "🧹 Limpiando artefactos de compilación..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -f fast_math*.so
	rm -f fast_math*.pyd
	find . -name "*.o" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Limpio"
