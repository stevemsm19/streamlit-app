import os

BASE_PATH = os.path.join(os.getcwd(), "src/data/temp_files")
print("BASE_PATH:", BASE_PATH)

SOURCES = {
    "Decreto 431 de 2024": os.path.join(BASE_PATH, "Decreto 431 de 2024.pdf"),
    "Decreto 154 de 2014": os.path.join(BASE_PATH, "Decreto 431-1 de 2024.pdf"),
    "Decreto 257 de 2021": os.path.join(BASE_PATH, "Decreto 257 de 2021.pdf"),
}
