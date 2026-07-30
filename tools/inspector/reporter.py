from .models import ProjectInventory


def print_report(inventory: ProjectInventory) -> None:
    separator = "=" * 46

    print()
    print("TENORIO3G FOUNDATION INSPECTOR")
    print(separator)
    print(f"Proyecto................. {inventory.project_name}")
    print("-" * 46)
    print(f"Archivos totales......... {inventory.total_files}")
    print(f"Archivos Python.......... {inventory.python_files}")
    print(f"Templates HTML........... {inventory.html_files}")
    print(f"Archivos CSS............. {inventory.css_files}")
    print(f"Archivos JavaScript...... {inventory.javascript_files}")
    print(f"Documentos Markdown...... {inventory.markdown_files}")
    print(f"Archivos vacíos.......... {inventory.empty_files}")
    print(separator)
    print("Inspección completada.")
    print()