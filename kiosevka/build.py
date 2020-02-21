#!/usr/bin/env python3

import os
import random
import subprocess
import zipfile


def docker_run(name: str, args: list = [], docker_build_args: list = [], docker_run_args: list = []):
    image_tag = f"{name}_{random.randrange(16**8)}"
    subprocess.check_call(["docker", "build", "-t", image_tag, *docker_build_args, "."])
    try:
        subprocess.check_call(["docker", "run", "-t", "--rm", *docker_run_args, image_tag, *args])
    finally:
        subprocess.check_call(["docker", "rmi", "-f", "--no-prune", image_tag])


def main():
    pwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pwd)

    docker_run(
        "foundry_kiosevka",
        ["ttf::kiosevka", "woff2::kiosevka"],
        ["--build-arg", "IOSEVKA_REF=v3.0.0-beta.3"],
        [
            "-v",
            f"{pwd}/build_plan.toml:/root/iosevka/private-build-plans.toml:ro",
            "-v",
            f"{pwd}/build:/root/iosevka/dist",
        ],
    )

    for dir in os.listdir("build/kiosevka"):
        with zipfile.ZipFile(f"build/kiosevka-{dir}.zip", "w", zipfile.ZIP_DEFLATED, 9) as zip:
            path = f"build/kiosevka/{dir}"
            for file in os.listdir(path):
                zip.write(f"{path}/{file}", f"kiosevka-{dir}/{file}")


if __name__ == "__main__":
    main()
