// =============================================================================
// fast_math.cpp — Módulo de alto rendimiento para Bourbaki Causal Engine
//
// Funciones expuestas a Python vía pybind11:
//   1. variance()                  — Varianza (Welford, O(n), numéricamente estable)
//   2. std_deviation()             — Desviación estándar
//   3. bayesian_normal_posterior() — Posterior conjugada Normal-Normal
//   4. bayesian_beta_posterior()   — Posterior conjugada Beta-Binomial
//   5. welford_online_stats()      — Media, varianza, count en pasada única
//
// Compilar:
//   python setup.py build_ext --inplace
//   # Genera: fast_math.cpython-311-x86_64-linux-gnu.so
// =============================================================================

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath>
#include <stdexcept>
#include <tuple>
#include <string>

namespace py = pybind11;

namespace bourbaki {

// =============================================================================
// 1. Welford's Online Algorithm — Varianza numéricamente estable O(n)
//    Evita catastrophic cancellation que ocurre con la fórmula naive
//    Ref: Welford, B. P. (1962). "Note on a method for calculating
//         corrected sums of squares and products"
// =============================================================================

struct WelfordState {
    long long count;
    double mean;
    double m2;  // Sum of squares of differences from the current mean

    WelfordState() : count(0), mean(0.0), m2(0.0) {}
};

WelfordState welford_accumulate(const std::vector<double>& data) {
    WelfordState state;
    for (const auto& x : data) {
        state.count++;
        double delta = x - state.mean;
        state.mean += delta / static_cast<double>(state.count);
        double delta2 = x - state.mean;
        state.m2 += delta * delta2;
    }
    return state;
}

// Varianza poblacional (N)
double variance(const std::vector<double>& data) {
    if (data.empty()) {
        throw std::invalid_argument("variance(): el array no puede estar vacío");
    }
    if (data.size() == 1) {
        return 0.0;
    }

    WelfordState state = welford_accumulate(data);
    return state.m2 / static_cast<double>(state.count);
}

// Varianza muestral (N-1) — Bessel's correction
double sample_variance(const std::vector<double>& data) {
    if (data.size() < 2) {
        throw std::invalid_argument(
            "sample_variance(): se necesitan al menos 2 elementos");
    }

    WelfordState state = welford_accumulate(data);
    return state.m2 / static_cast<double>(state.count - 1);
}

// Desviación estándar poblacional
double std_deviation(const std::vector<double>& data) {
    return std::sqrt(variance(data));
}

// Estadísticas online completas en una sola pasada
std::tuple<double, double, long long> welford_online_stats(
    const std::vector<double>& data
) {
    if (data.empty()) {
        throw std::invalid_argument(
            "welford_online_stats(): el array no puede estar vacío");
    }

    WelfordState state = welford_accumulate(data);
    double var = (state.count > 1)
        ? state.m2 / static_cast<double>(state.count)
        : 0.0;

    return std::make_tuple(state.mean, var, state.count);
}

// =============================================================================
// 2. Posterior Conjugada Normal-Normal
//    Prior:      μ ~ N(prior_mu, prior_sigma²)
//    Likelihood: x_i ~ N(μ, likelihood_sigma²)
//    Posterior:   μ | data ~ N(posterior_mu, posterior_sigma²)
//
//    Fórmulas cerradas (conjugacy):
//      posterior_sigma² = 1 / (1/prior_sigma² + n/likelihood_sigma²)
//      posterior_mu = posterior_sigma² * (prior_mu/prior_sigma² + n*x̄/likelihood_sigma²)
//
//    Ref: Murphy, K. P. (2007). "Conjugate Bayesian analysis of the
//         Gaussian distribution"
// =============================================================================

std::tuple<double, double> bayesian_normal_posterior(
    double prior_mu,
    double prior_sigma,
    const std::vector<double>& data,
    double likelihood_sigma
) {
    if (data.empty()) {
        throw std::invalid_argument(
            "bayesian_normal_posterior(): data no puede estar vacío");
    }
    if (prior_sigma <= 0.0 || likelihood_sigma <= 0.0) {
        throw std::invalid_argument(
            "bayesian_normal_posterior(): sigmas deben ser > 0");
    }

    const long long n = static_cast<long long>(data.size());

    // Media muestral (single pass)
    double data_mean = 0.0;
    for (const auto& x : data) {
        data_mean += x;
    }
    data_mean /= static_cast<double>(n);

    // Precisiones (inversa de varianza)
    double prior_precision      = 1.0 / (prior_sigma * prior_sigma);
    double likelihood_precision = static_cast<double>(n) / (likelihood_sigma * likelihood_sigma);

    // Posterior
    double posterior_precision = prior_precision + likelihood_precision;
    double posterior_sigma     = std::sqrt(1.0 / posterior_precision);
    double posterior_mu        = (prior_mu * prior_precision + data_mean * likelihood_precision)
                                 / posterior_precision;

    return std::make_tuple(posterior_mu, posterior_sigma);
}

// =============================================================================
// 3. Posterior Conjugada Beta-Binomial
//    Prior:      θ ~ Beta(alpha_prior, beta_prior)
//    Likelihood: k éxitos en n trials ~ Binomial(n, θ)
//    Posterior:   θ | data ~ Beta(alpha_prior + k, beta_prior + n - k)
//
//    Útil para: tasas de éxito, probabilidades de retención, conversion rates
//
//    Ref: Gelman, A. et al. (2013). "Bayesian Data Analysis", 3rd Ed.
// =============================================================================

std::tuple<double, double, double, double> bayesian_beta_posterior(
    double alpha_prior,
    double beta_prior,
    int successes,
    int trials
) {
    if (alpha_prior <= 0.0 || beta_prior <= 0.0) {
        throw std::invalid_argument(
            "bayesian_beta_posterior(): alpha y beta deben ser > 0");
    }
    if (successes < 0 || trials < 0 || successes > trials) {
        throw std::invalid_argument(
            "bayesian_beta_posterior(): se requiere 0 <= successes <= trials");
    }

    double alpha_post = alpha_prior + static_cast<double>(successes);
    double beta_post  = beta_prior + static_cast<double>(trials - successes);

    // Media y varianza de la distribución Beta posterior
    double posterior_mean     = alpha_post / (alpha_post + beta_post);
    double posterior_variance = (alpha_post * beta_post)
        / ((alpha_post + beta_post) * (alpha_post + beta_post)
           * (alpha_post + beta_post + 1.0));

    return std::make_tuple(alpha_post, beta_post, posterior_mean, posterior_variance);
}

}  // namespace bourbaki

// =============================================================================
// Binding pybind11 — Expone todo como módulo Python `fast_math`
// =============================================================================

PYBIND11_MODULE(fast_math, m) {
    m.doc() = R"pbdoc(
        Bourbaki Fast Math — Módulo C++ de alto rendimiento
        ===================================================

        Funciones optimizadas para cálculos estadísticos y bayesianos
        en el pipeline de inferencia causal.

        Compilado con pybind11 para interoperabilidad directa con Python/FastAPI.
    )pbdoc";

    // --- Estadísticas descriptivas ---
    m.def("variance", &bourbaki::variance,
        py::arg("data"),
        R"pbdoc(
            Calcula la varianza poblacional usando el algoritmo de Welford.
            Numéricamente estable, O(n), single-pass.

            Args:
                data: Lista de valores numéricos

            Returns:
                Varianza poblacional (float)

            Raises:
                ValueError: Si el array está vacío

            Example:
                >>> fast_math.variance([1.0, 2.0, 3.0, 4.0, 5.0])
                2.0
        )pbdoc");

    m.def("sample_variance", &bourbaki::sample_variance,
        py::arg("data"),
        R"pbdoc(
            Varianza muestral con corrección de Bessel (N-1).

            Args:
                data: Lista con al menos 2 valores

            Returns:
                Varianza muestral (float)
        )pbdoc");

    m.def("std_deviation", &bourbaki::std_deviation,
        py::arg("data"),
        R"pbdoc(
            Desviación estándar poblacional.

            Args:
                data: Lista de valores numéricos

            Returns:
                Desviación estándar (float)
        )pbdoc");

    m.def("welford_online_stats", &bourbaki::welford_online_stats,
        py::arg("data"),
        R"pbdoc(
            Estadísticas completas en una sola pasada (Welford).

            Returns:
                Tupla (mean, variance, count)
        )pbdoc");

    // --- Inferencia Bayesiana ---
    m.def("bayesian_normal_posterior", &bourbaki::bayesian_normal_posterior,
        py::arg("prior_mu"),
        py::arg("prior_sigma"),
        py::arg("data"),
        py::arg("likelihood_sigma"),
        R"pbdoc(
            Posterior conjugada Normal-Normal.

            Actualiza la creencia sobre μ dado nuevos datos observados.

            Args:
                prior_mu:         Media del prior N(μ₀, σ₀²)
                prior_sigma:      Desviación estándar del prior
                data:             Observaciones [x₁, x₂, ..., xₙ]
                likelihood_sigma: σ conocida del likelihood

            Returns:
                Tupla (posterior_mu, posterior_sigma)

            Example:
                >>> fast_math.bayesian_normal_posterior(0.0, 1.0, [0.5, 1.0, 1.5], 1.0)
                (0.75, 0.5)  # approximately
        )pbdoc");

    m.def("bayesian_beta_posterior", &bourbaki::bayesian_beta_posterior,
        py::arg("alpha_prior"),
        py::arg("beta_prior"),
        py::arg("successes"),
        py::arg("trials"),
        R"pbdoc(
            Posterior conjugada Beta-Binomial.

            Actualiza la creencia sobre θ (probabilidad de éxito) dado datos binomiales.

            Args:
                alpha_prior: Parámetro α del prior Beta(α, β)
                beta_prior:  Parámetro β del prior Beta(α, β)
                successes:   Número de éxitos observados (k)
                trials:      Número total de trials (n)

            Returns:
                Tupla (alpha_post, beta_post, posterior_mean, posterior_variance)

            Example:
                >>> fast_math.bayesian_beta_posterior(1.0, 1.0, 7, 10)
                (8.0, 4.0, 0.6667, 0.0171)  # approximately
        )pbdoc");

    // --- Versión ---
    m.attr("__version__") = "1.0.0";
    m.attr("__author__")  = "Bourbaki Engine Team";
}
