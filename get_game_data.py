import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]

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

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_name_from_path(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names

def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)

def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    with open(path, "w") as f:
        json.dump(data, f)

def run_command(command, path, code_file_name):
    cwd = os.getcwd()
    os.chdir(path)

    # compile the game
    run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)

    # run the game
    run_game_command = "./" + code_file_name
    run_game_command = os.path.splitext(run_game_command)[0]
    # print(run_game_command)
    result = run(run_game_command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print(run_game_command + ": " + " " + result.stdout)
    os.chdir(cwd)

def compile_and_run_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break

        break

    if code_file_name is None:
        return
    
    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command, path, code_file_name)

def main(source, target):
    # use path.join beause you are not sure what OS you are running. Different OS use different path divider
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_path(game_paths, "_game")

    create_dir(target_path)

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_and_run_game_code(dest_path)
    
    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)
    

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only.")
    
    source, target = args[1:]
    main(source, target)