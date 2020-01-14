#!/usr/bin/env python3

"""
Here's what this script does:
* Converts `specs.md` into a fancy specs html document (`frontend/public/specs.html`).
* Puts the javadoc in `frontend/public/javadoc/`.
* Builds the web client and copies it to `frontend/public/bc20`.

Only use this as part of following the `RELEASE.md` document. Crucially, `./gradlew publish` needs to run before this.
"""

import argparse
import subprocess
import os

def main():
    fancy_specs()

    javadoc()

    client()

def fancy_specs():
    os.chdir('specs')
    subprocess.call('pandoc specs.md --self-contained --template template.html --toc -o specs.html --metadata pagetitle="Battlecode 2020 Specs"', shell=True)
    os.chdir('..')
    subprocess.call('cp specs/specs.html frontend/public/specs.html', shell=True)

def javadoc():
    """
    Copy javadoc
    """
    subprocess.call("cp -r engine/build/docs/javadoc frontend/public", shell=True)

def client():
    """
    Build client for web.
    """
    os.chdir("client/visualizer")
    subprocess.call("npm run prod", shell=True)
    subprocess.call("cp -r bc20 ../../frontend/public", shell=True)
    os.chdir("../../frontend")

if __name__ == '__main__':
    main()
