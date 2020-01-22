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

INTERNAL_SCAFFOLD_PATH = '../battlecode20-internal-scaffold'
ENGINE_WORLD_PATH = 'engine/src/main/battlecode/world'

def main(version, maps, tournament):

    generate_comparison_link()

    specs(version)

    clientconfig(version)

    gradleprops(version)

    if maps:
        if tournament is not None:
            build_maps(tour=tournament)
        else:
            build_maps()
    
    if tournament is not None:
        update_tournament(tournament)

def update_tournament(tour):

    with open('client/visualizer/src/game/sidebar/mapfilter.ts', 'r') as f:
        cs = f.read()
    
    ll = []
    for l in cs.split('\n'):
        if l.strip().startswith('private readonly types: MapType[] '):
            ll.append(l[:-2] + ", MapType." + tour + "];")
        else:
            ll.append(l)
    cs = '\n'.join(ll)

    with open('client/visualizer/src/game/sidebar/mapfilter.ts', 'w') as f:
        f.write(cs)


def build_maps(tour='DEFAULT'):
    # copy from clipboard
    # assumes a list separated by \n, as if written in a google sheets column
    from pandas.io.clipboard import clipboard_get
    maplist = [x.strip() for x in clipboard_get().split('\n')]

    # copy the maps over from battlecode20-internal-scaffold
    for m in maplist:
        with open(INTERNAL_SCAFFOLD_PATH + '/src/maps/' + m + '.java', 'r') as f:
            mp = f.read()
        # change the package name
        mp = mp.replace('package maps', 'package battlecode.world.maps')
        # change the path
        mp = mp.replace('public static final String outputDirectory = "maps/";', 'public static final String outputDirectory = "engine/src/main/battlecode/world/resources/";')
        # write to maps
        with open('engine/src/main/battlecode/world/maps/' + m + '.java', 'w') as f:
            f.write(mp)

    # add the maps to BuildMaps.java
    with open(ENGINE_WORLD_PATH + "/BuildMaps.java", "r") as f:
        bmps = f.read()
    
    bmps = bmps.replace('public static void main(String[] args) {', 'public static void main(String[] args) {\n' + '\n'.join(['        ' + m + '.main(args);' for m in maplist]))

    with open(ENGINE_WORLD_PATH + "/BuildMaps.java", "w") as f:
        f.write(bmps)

    # build the maps
    os.system('./gradlew buildMaps')

    # now update SERVER_MAPS in client/visualizer/constants.ts
    with open('client/visualizer/src/constants.ts', 'r') as f:
        cs = f.read()
    
    cs = cs.replace('export const SERVER_MAPS: Map<string, MapType> = new Map<string, MapType>([', 'export const SERVER_MAPS: Map<string, MapType> = new Map<string, MapType>([\n' + '\n'.join(['  ["' + m  + '", MapType.' + tour + '],' for m in maplist]))

    with open('client/visualizer/src/constants.ts', 'w') as f:
        f.write(cs)
    
    # now update backend/settings.py
    with open('backend/settings.py', 'r') as f:
        cs = f.read()
    
    cs = cs.replace('SERVER_MAPS = [', 'SERVER_MAPS = [\n' + '\n'.join(['  "' + m + '",' for m in maplist]))

    with open('backend/settings.py', 'w') as f:
        f.write(cs)



def generate_comparison_link():
    """
    Generate a comparison link like https://github.com/battlecode/battlecode20/compare/commit...commit
    comparing the most recent commit with the latest released version.
    """
    # get latest tag
    latest_tag = subprocess.check_output("git tag --sort=committerdate | tail -1", shell=True).decode("utf-8").strip('\n')
    # get commit
    commit = subprocess.check_output("git rev-list -n 1 " + latest_tag, shell=True).decode('utf-8').strip('\n')

    # get latest commit
    latest = subprocess.check_output("git rev-parse HEAD", shell=True).decode('utf-8').strip('\n')

    # print the link
    link = "https://github.com/battlecode/battlecode20/compare/" + commit + "..." + latest
    print("Go to the following link and check out the differences:")
    print(link)

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
    parser.add_argument('--maps', default=False,
                    help='whether maps should be built and copied')
    parser.add_argument('--tournament', default=None,
                    help='tournament name: one of DEFAULT,SPRINT,SEEDING,INTL_QUALIFYING,US_QUALIFYING,HS,NEWBIE,FINAL,CUSTOM')

    args = parser.parse_args()

    main(args.version, args.maps, args.tournament)
