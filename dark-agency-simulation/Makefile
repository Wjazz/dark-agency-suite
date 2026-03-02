# Dark Agency Simulation - Makefile
# Build system for the C++ simulation

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
DEBUG_FLAGS = -g -DDEBUG

SRC_DIR = src
BIN_DIR = bin
OUTPUT_DIR = output

# Source files
SOURCES = $(SRC_DIR)/main.cpp
HEADERS = $(SRC_DIR)/config.hpp \
          $(SRC_DIR)/cell.hpp \
          $(SRC_DIR)/random.hpp \
          $(SRC_DIR)/grid.hpp \
          $(SRC_DIR)/agent.hpp \
          $(SRC_DIR)/statistics.hpp \
          $(SRC_DIR)/simulation.hpp

TARGET = $(BIN_DIR)/dark-agency-sim

# Default target
all: dirs $(TARGET)

# Create directories
dirs:
	@mkdir -p $(BIN_DIR)
	@mkdir -p $(OUTPUT_DIR)

# Build main executable
$(TARGET): $(SOURCES) $(HEADERS)
	$(CXX) $(CXXFLAGS) $(SOURCES) -o $(TARGET)

# Debug build
debug: CXXFLAGS += $(DEBUG_FLAGS)
debug: dirs $(TARGET)

# Run simulation
run: all
	./$(TARGET)

# Run in fast mode (no visualization)
fast: all
	./$(TARGET) --fast

# Clean build files
clean:
	rm -rf $(BIN_DIR)
	rm -f $(OUTPUT_DIR)/*.csv $(OUTPUT_DIR)/*.txt

# Clean and rebuild
rebuild: clean all

# Help target
help:
	@echo "Dark Agency Simulation - Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all      - Build simulation (default)"
	@echo "  debug    - Build with debug symbols"
	@echo "  run      - Build and run with visualization"
	@echo "  fast     - Build and run without visualization"
	@echo "  clean    - Remove build files"
	@echo "  rebuild  - Clean and rebuild"
	@echo "  help     - Show this help"
	@echo ""
	@echo "Usage:"
	@echo "  make           # Build"
	@echo "  make run       # Build and run"
	@echo "  make fast      # Quick analysis without visuals"

.PHONY: all dirs debug run fast clean rebuild help
