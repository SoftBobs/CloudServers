import os
import sys

def get_resource_path():
    if getattr(sys, 'frozen', False):
        # Путь в среде исполняемого файла
        base_path = sys._MEIPASS
    else:
        # Путь в среде разработки
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, 'os_service_types', 'data', 'service-types.json')
