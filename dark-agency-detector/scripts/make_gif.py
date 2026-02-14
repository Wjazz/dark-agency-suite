#!/usr/bin/env python3
"""
DarkAgencyDetector - GIF Animation Generator

Converts exported PPM frames into an animated GIF.
Requires: Pillow (pip install Pillow)
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow no está instalado.")
    print("Instalar con: pip install Pillow")
    sys.exit(1)


def load_ppm_frames(frames_dir: str) -> list:
    """Load all PPM frames from directory"""
    frames_path = Path(frames_dir)
    if not frames_path.exists():
        print(f"Error: Directorio {frames_dir} no existe")
        return []
    
    frame_files = sorted(frames_path.glob("frame_*.ppm"))
    
    if not frame_files:
        print(f"Error: No se encontraron frames en {frames_dir}")
        return []
    
    print(f"Cargando {len(frame_files)} frames...")
    
    frames = []
    for i, f in enumerate(frame_files):
        try:
            img = Image.open(f)
            frames.append(img.copy())
            img.close()
            
            if (i + 1) % 20 == 0:
                print(f"  Procesados: {i + 1}/{len(frame_files)}")
        except Exception as e:
            print(f"  Error cargando {f}: {e}")
    
    return frames


def create_gif(frames: list, output_path: str, duration: int = 100, loop: int = 0):
    """Create animated GIF from frames"""
    if not frames:
        return False
    
    print(f"\nCreando GIF: {output_path}")
    print(f"  Frames: {len(frames)}")
    print(f"  Duration: {duration}ms por frame")
    
    # Convert to palette mode for GIF
    frames_p = []
    for frame in frames:
        # Ensure RGB mode
        if frame.mode != 'RGB':
            frame = frame.convert('RGB')
        # Quantize to 256 colors for GIF
        frames_p.append(frame.quantize(colors=256, method=Image.Quantize.MEDIANCUT))
    
    # Save as GIF
    frames_p[0].save(
        output_path,
        save_all=True,
        append_images=frames_p[1:],
        optimize=False,
        duration=duration,
        loop=loop
    )
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  Tamaño: {file_size:.2f} MB")
    print(f"\n✓ GIF creado exitosamente: {output_path}")
    
    return True


def create_legend_image(output_path: str):
    """Create a legend image for the GIF"""
    try:
        from PIL import ImageDraw, ImageFont
    except ImportError:
        return
    
    width = 400
    height = 200
    img = Image.new('RGB', (width, height), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((20, 10), "DARK AGENCY DETECTOR", fill=(255, 255, 255))
    draw.text((20, 30), "Agent-Based Simulation", fill=(150, 150, 150))
    
    # Legend entries
    y = 60
    entries = [
        ((0, 255, 200), "🔵 Dark Innovator (High S_Agency, Low G)"),
        ((255, 200, 0), "🟡 Maverick at Risk (Transitional)"),
        ((255, 60, 60), "🔴 Toxic (High G)"),
        ((100, 150, 255), "⚪ Normal (Low S_Agency, Low G)"),
    ]
    
    for color, text in entries:
        draw.ellipse([20, y, 35, y+15], fill=color)
        draw.text((45, y), text, fill=(200, 200, 200))
        y += 25
    
    img.save(output_path)
    print(f"✓ Legend saved: {output_path}")


def main():
    # Paths
    script_dir = Path(__file__).parent.parent
    frames_dir = script_dir / "frames"
    output_dir = script_dir / "output"
    
    output_dir.mkdir(exist_ok=True)
    
    output_gif = output_dir / "dark_agency_simulation.gif"
    legend_path = output_dir / "legend.png"
    
    print("=" * 60)
    print("  DARK AGENCY DETECTOR - GIF Generator")
    print("=" * 60)
    print()
    
    # Load frames
    frames = load_ppm_frames(str(frames_dir))
    
    if not frames:
        print("\nNo frames to process. Run the simulation first:")
        print("  ./bin/dark-agency-detector")
        return 1
    
    # Create GIF
    success = create_gif(frames, str(output_gif), duration=80)
    
    if success:
        # Create legend
        create_legend_image(str(legend_path))
        
        print("\n" + "=" * 60)
        print("  EL 'FLEX' ESTÁ LISTO")
        print("=" * 60)
        print()
        print("Archivo GIF:", output_gif)
        print()
        print('"Mira esto. Programé una simulación en C++ donde cada agente')
        print('tiene un nivel de Maquiavelismo y Agencia. Los puntos cian son')
        print('los Dark Innovators - nosotros rompiendo burocracia."')
        print()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
