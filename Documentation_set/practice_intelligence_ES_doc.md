1. ## Visión General:
Este archivo contiene la lógica para generar reglas de evaluación específicas para la práctica basadas en el tipo de directorio (por ejemplo, Chambers, Legal500) y el área de práctica. Su objetivo es proporcionar orientación adaptada sobre qué aspectos del trabajo legal destacar para diferentes directorios.

2. ## Clases:
No hay clases definidas en el fragmento de código proporcionado.

3. ## Funciones y Métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `get_practice_rules` | `practice_area`: str, `directory_type`: str | Devuelve la lógica de evaluación universal basada en el área de práctica y el tipo de directorio. Normaliza el área de práctica a mayúsculas y aplica lógica condicional para generar cadenas de reglas específicas para los directorios Chambers y Legal500. Si no se encuentran reglas específicas, devuelve un mensaje estándar o predeterminado. |