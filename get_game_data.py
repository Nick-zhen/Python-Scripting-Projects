import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"

def find_all_game_paths(source):
    game_paths = []

    # since we only need the first level of dir, we only need this run one time
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break

    return game_paths

def main(source, target):
    # use path.join beause you are not sure what OS you are running. Different OS use different path divider
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    print(game_paths)

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only.")
    
    source, target = args[1:]
    main(source, target)