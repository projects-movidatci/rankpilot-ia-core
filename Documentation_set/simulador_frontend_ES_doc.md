Aquí tienes la traducción del Markdown proporcionado al español, manteniendo las directrices:

1. ## Visión general:
Este archivo simula una interfaz de línea de comandos (CLI) para el frontend de RankPilot. Permite a los usuarios iniciar un trabajo de procesamiento proporcionando la entrada de tres maneras: cargando un documento, pegando texto sin formato o comenzando con un lienzo en blanco. El simulador luego consulta un backend de FastAPI para el estado del trabajo, muestra el progreso y maneja los resultados, incluyendo el análisis estratégico y las posibles preguntas de seguimiento.

2. ## Clases:
No hay clases explícitas definidas en este script.

3. ## Funciones y Métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `print_header` | `texto` | Imprime un encabezado formateado con un texto dado, rodeado por líneas de caracteres '=' para una separación visual. |
| `main` | None | Orquesta la simulación de la CLI. Presenta opciones de entrada al usuario, prepara el `agent_state` inicial, envía la primera solicitud al backend de FastAPI y entra en un bucle para consultar el estado del trabajo y manejar las respuestas hasta que el trabajo se complete o falle. También procesa y muestra el análisis estratégico final y las interacciones de la sala de auditoría. |