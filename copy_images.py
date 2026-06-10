import shutil
import os
from pathlib import Path

src_dir = r"D:\Homelab\site\gdocs with image"
dest_dir = r"D:\Homelab\site\jekyll-theme-chirpy-7.5.0\assets\img\posts\active-directory"

# Create destination
os.makedirs(dest_dir, exist_ok=True)

# Copy all PNG files
src_path = Path(src_dir)
for png_file in src_path.glob("*.png"):
    shutil.copy2(str(png_file), os.path.join(dest_dir, png_file.name))
    print(f"Copied: {png_file.name}")

print(f"\nTotal files copied: {len(list(Path(dest_dir).glob('*.png')))}")