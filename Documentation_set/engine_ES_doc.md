1. ## Descripción general:
Este archivo define la clase `VRAMManager`, responsable de la gestión de la asignación y el seguimiento de los recursos de memoria de video (VRAM) dentro de una aplicación. Permite la asignación y desasignación de bloques de VRAM, con la capacidad de monitorear el uso actual y prevenir desbordamientos.

2. ## Clases:
* **VRAMManager**: Gestiona la asignación, desasignación y monitoreo de uso de VRAM.

3. ## Funciones y métodos:

| Nombre              | Parámetros      | Responsabilidad                                                                                   |
|---------------------|-----------------|---------------------------------------------------------------------------------------------------|
| `__init__`          | `total_vram_mb` | Inicializa el VRAMManager con la VRAM total disponible en megabytes. Establece la VRAM asignada y libre inicial a cero. |
| `allocate_vram`     | `size_mb`       | Intenta asignar una cantidad especificada de VRAM. Devuelve `True` si tiene éxito, `False` en caso contrario. |
| `deallocate_vram`   | `size_mb`       | Desasigna una cantidad especificada de VRAM.                                                        |
| `calculate_vram_usage`|                 | Calcula el uso actual de VRAM en megabytes.                                                        |
| `get_free_vram`     |                 | Devuelve la cantidad de VRAM libre en megabytes.                                                    |
| `is_vram_sufficient`| `required_mb`   | Comprueba si hay suficiente VRAM libre para cumplir un requisito dado. Devuelve `True` si es suficiente, `False` en caso contrario. |