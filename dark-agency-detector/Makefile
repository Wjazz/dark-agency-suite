# DarkAgencyDetector - Makefile

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
DEBUG_FLAGS = -g -DDEBUG

SRC_DIR = src
BIN_DIR = bin
OUTPUT_DIR = output
FRAMES_DIR = frames

SOURCES = $(SRC_DIR)/main.cpp
HEADERS = $(wildcard $(SRC_DIR)/*.hpp)

TARGET = $(BIN_DIR)/dark-agency-detector

.PHONY: all dirs debug run fast clean rebuild gif help

all: dirs $(TARGET)

dirs:
	@mkdir -p $(BIN_DIR)
	@mkdir -p $(OUTPUT_DIR)
	@mkdir -p $(FRAMES_DIR)

$(TARGET): $(SOURCES) $(HEADERS)
	$(CXX) $(CXXFLAGS) $(SOURCES) -o $(TARGET)
	@echo "✓ Build complete: $(TARGET)"

debug: CXXFLAGS += $(DEBUG_FLAGS)
debug: dirs $(TARGET)

run: all
	./$(TARGET)

fast: all
	./$(TARGET) --fast

gif: all
	./$(TARGET) --fast
	python3 scripts/make_gif.py

clean:
	rm -rf $(BIN_DIR)
	rm -f $(OUTPUT_DIR)/*.csv $(OUTPUT_DIR)/*.txt $(OUTPUT_DIR)/*.gif
	rm -f $(FRAMES_DIR)/*.ppm

rebuild: clean all

help:
	@echo "DarkAgencyDetector - Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all     - Build (default)"
	@echo "  run     - Build and run with visualization"
	@echo "  fast    - Run fast (no visualization)"
	@echo "  gif     - Run and generate GIF animation"
	@echo "  clean   - Remove all generated files"
	@echo "  help    - Show this help"
	@echo ""
	@echo "Quick start:"
	@echo "  make gif    # Build, simulate, and create GIF"
