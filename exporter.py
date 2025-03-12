import os
# Списки для игнорируемых файлов и директорий
ignore_files = ['.gitignore']  # Добавьте сюда файлы, которые нужно игнорировать
ignore_dirs = ['__pycache__', '.venv', '.git', '.idea', 'log_dir']  # Добавьте сюда папки, которые нужно игнорировать


def generate_report(root_dir):
    project_report = []

    def process_directory(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)

            # Проверяем, нужно ли игнорировать файл или директорию
            if os.path.isfile(item_path):
                if item in ignore_files:
                    continue
                project_report.append(f"Файл: {item_path}")
                try:
                    with open(item_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        project_report.append(f"Содержимое файла {item}:\n{content}\n{'-' * 50}")
                except Exception as e:
                    project_report.append(f"Не удалось прочитать файл {item}: {e}\n")
            elif os.path.isdir(item_path):
                if item in ignore_dirs:
                    continue
                project_report.append(f"Директория: {item_path}")
                process_directory(item_path)

    project_report.append(f"Отчет о проекте в директории: {root_dir}\n{'=' * 50}")
    process_directory(root_dir)
    return "\n".join(project_report)


if __name__ == "__main__":
    project_root = 'D:\\Work\\Python\\calendar_bot_new\\'

    if not os.path.exists(project_root):
        print("Указанный путь не существует.")
    else:
        report = generate_report(project_root)
        print(report)

        # Сохранение отчета в файл
        output_file = project_root + "project_report.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Отчет успешно сохранен в файл: {output_file}")