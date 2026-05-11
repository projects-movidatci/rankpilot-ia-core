1. ## Resumen:
Este archivo orquesta la ejecución de un flujo de trabajo de varias etapas para procesar envíos legales, simulando un entorno de prueba local para el sistema RankPilot. Maneja la entrada de documentos, la gestión de estados, las preguntas interactivas y la generación de la salida final, incluyendo un diagnóstico estratégico y un documento de envío ensamblado.

2. ## Clases:
* `AgentState`: Representa el estado actual del agente/flujo de trabajo, conteniendo información como detalles del envío, metadatos, documentos, historial y progreso actual.
* `MetaData`: Contiene metadatos asociados a un envío, como directorio, guía, región, jurisdicción, área de práctica y nombre de la firma.

3. ## Funciones y Métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `main` | Ninguno | El punto de entrada del script. Inicializa el flujo de trabajo, simula un envío de usuario con un documento o texto sin formato, procesa el envío a través de múltiples etapas del flujo de trabajo (incluyendo el llenado interactivo de lagunas), imprime información de diagnóstico y guarda el documento ensamblado final. |