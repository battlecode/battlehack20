#!/usr/bin/env python3

"""
Here's what this script does:
* Adds version number and changelog to specs/specs.md
* Adds version number to client/visualizer/src/config.ts
* Adds version number to gradle.properties

Run this before `./gradlew publish`.
"""

import argparse
import subprocess
import os
from datetime import datetime

def main(version):

    specs(version)

    clientconfig(version)

    gradleprops(version)

def specs(version):
    with open('specs/specs.md', 'r') as f:
        gr = f.read()

    # prompt for changelog in specs, engine, client
    l = ['spec', 'client', 'engine']
    d = {i: [] for i in l}
    for i in l:
        while True:
            x = input(i + " change: ")
            if x == "":
                break
            d[i].append(x)
    now = datetime.now()
    changelogstring = "- " + version + " (" + str(now.month) + "/" + str(now.day) + "/" + str(now.year)[2:] + ")\n"
    for i in l:
        changelogstring += "    - " + i + " changes:"
        if len(d[i]) == 0:
            changelogstring += " none\n"
        else:
            changelogstring += "\n"
        for dd in d[i]:
            changelogstring += "        - " + dd + '\n'
    g = gr.split('\n')
    for i in range(len(g)):
        if "# Changelog" in g[i]:
            g.insert(i+2, changelogstring.rstrip())
        if "Current version: " in g[i]:
            g[i] = "Current version: " + version
    gr = "\n".join(g)
    with open('specs/specs.md', 'w') as f:
        f.write(gr)

def gradleprops(version):
    with open('gradle.properties', 'r') as f:
        gr = f.read()
    g = gr.split('\n')
    for i in range(len(g)):
        if "release_version" in g[i]:
            p = g[i].split('=')
            g[i] = "release_version=" + version
    gr = "\n".join(g)
    with open('gradle.properties', 'w') as f:
        f.write(gr)

def clientconfig(version):
    with open('client/visualizer/src/config.ts', 'r') as f:
        client_config = f.read()
    config_lines = client_config.split('\n')
    for i in range(len(config_lines)):
        if "Change this on each release!" in config_lines[i]:
            p = config_lines[i].split('"')
            config_lines[i] = p[0] + '"' + version + '"' + p[2]
    client_config = "\n".join(config_lines)
    with open('client/visualizer/src/config.ts', 'w') as f:
        f.write(client_config)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('version', help='Version number, e.g. 2020.0.1.1')

    args = parser.parse_args()

    main(args.version)
