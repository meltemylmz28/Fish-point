#!/usr/bin/env python
import os
import sys
from pathlib import Path


def main():
    """Yönetimsel görevleri çalıştırır."""
    # Proje kök dizinini (backend) Python yoluna ekler
    base_dir = Path(__file__).resolve().parent
    if str(base_dir) not in sys.path:
        sys.path.append(str(base_dir))

    # Ayarlar modülünü tanımlar
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django içe aktarılamadı. Sanal ortamın aktif olduğundan emin misiniz?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()