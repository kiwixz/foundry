#!/usr/bin/env python3

import os
import shutil
import subprocess
import zipfile


IMAGE_TAG = "foundry_kiosevka"
IOSEVKA_REF = "v4.0.0"
VERSION = "2.0.0"


def build():
    subprocess.check_call(["docker", "build", "-t", IMAGE_TAG, "--build-arg", f"IOSEVKA_REF={IOSEVKA_REF}", "."])
    container_id = subprocess.check_output(["docker", "create", IMAGE_TAG]).decode().rstrip()
    try:
        os.makedirs("build", exist_ok=True)
        for ext in ["ttf", "woff2"]:
            out_dir = f"build/{ext}"
            if os.path.exists(out_dir):
                shutil.rmtree(out_dir)
            subprocess.check_call(["docker", "cp", f"{container_id}:/root/iosevka/dist/kiosevka/{ext}", out_dir])
    finally:
        subprocess.check_call(["docker", "rm", container_id])


def package():
    for ext in ["ttf", "woff2"]:
        fullname = f"kiosevka-{ext}-{VERSION}"
        with zipfile.ZipFile(f"build/{fullname}.zip", "w", zipfile.ZIP_DEFLATED, compresslevel=9) as arc:
            path = f"build/{ext}"
            for file in os.listdir(path):
                arc.write(f"{path}/{file}", f"{fullname}/{file}")


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    build()
    package()


if __name__ == "__main__":
    main()
