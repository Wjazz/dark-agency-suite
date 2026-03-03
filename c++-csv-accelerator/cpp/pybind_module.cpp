#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>

// Declaración de la función que está en csv_reader.cpp
std::vector<double> parse_numeric_column(const std::string &path, size_t column_index, char delim=',');

namespace py = pybind11;

py::list read_col_as_list(const std::string &path, int col) {
    auto vec = parse_numeric_column(path, (size_t)col);
    py::list out;
    for (double v: vec) out.append(v);
    return out;
}

PYBIND11_MODULE(csv_accel, m) {
    m.doc() = "CSV accelerator minimal";
    m.def("read_col_as_list", &read_col_as_list, "Read numeric column as python list", py::arg("path"), py::arg("col"));
}
