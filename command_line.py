import tarfile
import argparse
import xml.etree.ElementTree as ET
import csv
import time
from datetime import datetime
import platform


class VirtualFileSystem:
    def __init__(self, tar_path, user_name, hostname):
        self.tar_path = tar_path
        self.user_name=user_name
        self.hostname=hostname
        self.current_dir = '/'
        self.file_structure = {}
        self.start_time = time.time()
        self.load_tar()

    def load_tar(self):
        with tarfile.open(self.tar_path, 'r') as tar:
            for member in tar.getmembers():
                parts = member.name.strip('/').split('/')
                current_level = self.file_structure
                for part in parts:
                    is_file = part == parts[-1] and not member.isdir()
                    if is_file:
                        current_level[part] = {
                            "type": "file"
                        }
                    else:
                        if part not in current_level:
                            current_level[part] = {
                                "type": "folder",
                                "list_f": {}
                            }
                        current_level = current_level[part]["list_f"]

    def cd(self, path):
        if path == '~':
            self.current_dir = '/'
            return
        parsed_path = self.path_parser(path)
        if self.get_directory_from_absolute_path(parsed_path) is None:
            print(f"cd: {path}: такого каталога нет")
        else:
            self.current_dir = parsed_path

    def path_parser(self, path):
        if path.startswith("/"):
            abs_path = path
        else:
            abs_path = self.current_dir + path

        parts = abs_path.split('/')
        final_parts = []
        for part in parts:
            if part == '' or part == '.':
                continue
            elif part == "..":
                if final_parts:
                    final_parts.pop()
            else:
                final_parts.append(part)

        final_path = '/' + '/'.join(final_parts) + '/'
        final_path = final_path.replace('//', '/')
        if final_path == '':
            final_path = '/'
        return final_path

    def get_directory_from_absolute_path(self, path):
        if path == "/":
            return self.file_structure
        parts = path.strip('/').split('/')
        current_level = self.file_structure
        for part in parts:
            if part in current_level:
                if current_level[part]["type"] == "folder":
                    current_level = current_level[part]["list_f"]
                else:
                    return None
            else:
                return None
        return current_level

    def ls(self, path="."):
        parsed_path = self.path_parser(path)
        directory_dict = self.get_directory_from_absolute_path(parsed_path)
        if directory_dict is None:
            print(f"ls: {path}: такого каталога нет")
            return []

        return list(directory_dict.keys())

    def uptime(self):
        current_time = time.time()
        uptime_seconds = current_time - self.start_time
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Текущее время: {current_time_str}, Время работы: {uptime_seconds:.2f} секунд"

    def uname(self):
        return (
        f"Система: { platform.system()}\n"
        f"Имя узла: {platform.node()}\n"
        f"Версия: {platform.release()}\n"
        f"Полная версия: {platform.version()}\n"
        f"Архитектура: {platform.machine()}\n"
        f"Процессор: {platform.processor()}\n"
        )



    def who(self):
        return self.user_name


def log_action(log_file, username, action):
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), username, action])


def execute_startup_script(vfs, script_file):
    try:
        with open(script_file, 'r') as f:
            commands = f.readlines()
            for command in commands:
                command = command.strip()
                if command:
                    shell_command(vfs, command)
    except FileNotFoundError:
        print(f"Стартовый скрипт {script_file} не найден.")


def shell_command(vfs, command):
    parts = command.split()
    cmd = parts[0]
    args = parts[1:]

    if cmd == "exit":
        return False
    elif cmd == "cd":
        if len(args) == 1:
            vfs.cd(args[0])
        else:
            print("Команда cd требует один аргумент.")
    elif cmd == "ls":
        directory_list = vfs.ls(args[0] if args else ".")
        print("\n".join(directory_list))
    elif cmd == "uptime":
        print(vfs.uptime())
    elif cmd == "uname":
        print(vfs.uname())
    elif cmd == "who":
        print(vfs.who())
    else:
        print(f"{cmd}: команда не найдена.")

    return True


def main(config_file):
    tree = ET.parse(config_file)
    root = tree.getroot()

    username = root.find('username').text
    hostname = root.find('hostname').text
    tar_path = root.find('tar_path').text
    log_file = root.find('log_file').text
    startup_script = root.find('startup_script').text


    vfs = VirtualFileSystem(tar_path, username, hostname)

    execute_startup_script(vfs, startup_script)

    while True:
        print(f"{username}@{hostname}:{vfs.current_dir}$ ", end="")
        line = input().strip()

        if not line:
            continue

        log_action(log_file, username, line)

        if not shell_command(vfs, line):
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Эмулятор оболочки UNIX-подобной ОС.")
    parser.add_argument("config_file", help="Путь к конфигурационному файлу в формате XML.")
    args = parser.parse_args()

    main(args.config_file)
