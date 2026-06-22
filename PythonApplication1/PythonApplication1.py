import threading
import queue
import os
from datetime import datetime


# Симуляция простого ядра операционной системы
class Kernel:
    def __init__(self, device_folder, log_file):
        self.process_queue = queue.Queue()
        self.file_system = FileSystem(device_folder, log_file)
        self.device = VirtualDevice(log_file)
        self.log_file = log_file
        self.log("Ядро инициализировано.")

    def log(self, message):
        with open(self.log_file, "a") as log:
            log.write(f"{datetime.now()} - {message}\n")

    def create_process(self, process_name, func, *args):
        process = threading.Thread(target=func, args=args, name=process_name)
        self.process_queue.put(process)
        self.log(f"Создан процесс: {process_name}")

    def run(self):
        self.log("Запуск процессов...")
        while not self.process_queue.empty():
            process = self.process_queue.get()
            self.log(f"Выполняется процесс: {process.name}")
            process.start()
            process.join()
            self.log(f"Процесс завершён: {process.name}")


# Симуляция файловой системы
class FileSystem:
    def __init__(self, device_folder, log_file):
        self.device_folder = device_folder
        self.log_file = log_file
        os.makedirs(device_folder, exist_ok=True)

    def log(self, message):
        with open(self.log_file, "a") as log:
            log.write(f"{datetime.now()} - {message}\n")

    def create_file(self, filename, content):
        file_path = os.path.join(self.device_folder, filename)
        with open(file_path, "w") as file:
            file.write(content)
        self.log(f"Файл создан: {file_path}")
        print(f"[FileSystem] Файл создан: {file_path}")

    def read_file(self, filename):
        file_path = os.path.join(self.device_folder, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                content = file.read()
            self.log(f"Файл прочитан: {file_path}")
            print(f"[FileSystem] Файл прочитан: {file_path}")
            return content
        else:
            self.log(f"Файл не найден: {file_path}")
            print(f"[FileSystem] Ошибка: файл {file_path} не найден!")
            return None


# Симуляция виртуального устройства
class VirtualDevice:
    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, message):
        with open(self.log_file, "a") as log:
            log.write(f"{datetime.now()} - {message}\n")

    def write(self, data):
        self.log(f"Данные записаны на устройство: {data}")
        print(f"[Device] Данные записаны на устройство: {data}")

    def read(self):
        self.log("Данные считаны с устройства.")
        print("[Device] Данные считаны с устройства.")
        return "Тестовые данные"


# Процессы
def write_to_file(kernel, filename, content):
    kernel.file_system.create_file(filename, content)


def read_from_file(kernel, filename):
    content = kernel.file_system.read_file(filename)
    if content:
        print(f"[Process] Содержимое файла {filename}: {content}")


def device_interaction(kernel, data):
    kernel.device.write(data)
    received_data = kernel.device.read()
    print(f"[Process] Получено с устройства: {received_data}")


# Меню управления
def menu():
    device_folder = "device_files"
    log_file = "kernel_logs.txt"
    kernel = Kernel(device_folder, log_file)

    while True:
        print("\n--- Меню ---")
        print("1. Создать файл")
        print("2. Прочитать файл")
        print("3. Взаимодействие с устройством")
        print("4. Запустить процессы")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            filename = input("Введите имя файла: ")
            content = input("Введите содержимое файла: ")
            kernel.create_process("WriteProcess", write_to_file, kernel, filename, content)
        elif choice == "2":
            filename = input("Введите имя файла для чтения: ")
            kernel.create_process("ReadProcess", read_from_file, kernel, filename)
        elif choice == "3":
            data = input("Введите данные для устройства: ")
            kernel.create_process("DeviceProcess", device_interaction, kernel, data)
        elif choice == "4":
            kernel.run()
        elif choice == "5":
            print("Завершение программы.")
            kernel.log("Программа завершена.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    menu()