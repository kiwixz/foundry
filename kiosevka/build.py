#!/usr/bin/env python3

import os
import random
import subprocess


def docker_run(name: str, args: list = [], docker_args: list = []):
    image_tag = f"{name}_{random.randrange(16**8)}"
    subprocess.check_call(["docker", "build", "-t", image_tag, "."])
    try:
        subprocess.check_call(["docker", "run", "-t", *docker_args, "--rm", image_tag, *args])
    finally:
        subprocess.check_call(["docker", "rmi", "-f", "--no-prune", image_tag])


def main():
    pwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pwd)

    docker_run(
        "foundry_kiosevka",
        ["ttf::kiosevka", "woff2::kiosevka"],
        [
            "-v",
            f"{pwd}/build_plan.toml:/root/iosevka/private-build-plans.toml:ro",
            "-v",
            f"{pwd}/build:/root/iosevka/dist",
        ],
    )


if __name__ == "__main__":
    main()
