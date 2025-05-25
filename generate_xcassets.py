import os
import sys
import shutil
import json
from pathlib import Path

def generate_imageset(name, files, output_dir):
    imageset_path = output_dir / f"{name}.imageset"
    imageset_path.mkdir(parents=True, exist_ok=True)

    images_json = []

    for scale in ['1x', '2x', '3x']:
        match = next((f for f in files if f.endswith(f"@{scale}.png")), None)
        if match:
            dest = imageset_path / os.path.basename(match)
            shutil.copy(match, dest)
            images_json.append({
                "idiom": "universal",
                "filename": os.path.basename(match),
                "scale": scale
            })

    contents = {
        "images": images_json,
        "info": {
            "version": 1,
            "author": "xcode"
        }
    }

    with open(imageset_path / "Contents.json", "w") as f:
        json.dump(contents, f, indent=2)

def main(input_folder, output_folder):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    grouped = {}
    for file in input_path.glob("*.png"):
        base = file.name.split("@")[0].replace(".png", "")
        grouped.setdefault(base, []).append(str(file))

    for name, files in grouped.items():
        generate_imageset(name, files, output_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: generate_xcassets.py input-folder output-folder")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
