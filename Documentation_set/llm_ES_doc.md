1. ## Resumen:
Este archivo actúa como una fábrica para crear instancias de `ChatOpenAI`, configuradas para diferentes entornos (local o de producción) y proveedores de LLM (OpenAI u OpenRouter). Soporta el registro opcional de mensajes de diagnóstico en un diccionario `updates`.

2. ## Clases:
No hay clases definidas en este archivo.

3. ## Funciones y Métodos:

| Nombre         | Parámetros                                        | Responsabilidad                                                                                                                                                                                                                         |
| -------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_llm`      | `temperature` (float, por defecto 0.2), `updates` (dict, por defecto None) | Devuelve una instancia de `ChatOpenAI`. Detecta la variable `ENVIRONMENT`. Para el entorno "local", utiliza OpenRouter con un modelo Gemini. Para otros entornos (producción), utiliza OpenAI con un modelo `gpt-5.4-mini`. Opcionalmente añade detalles del entorno y la clave API a la lista `updates["messages"]`. |
| `get_llm_2`    | `temperature` (float, por defecto 0.0), `updates` (dict, por defecto None) | Devuelve una instancia de `ChatOpenAI` específicamente para tareas de clasificación. Detecta la variable `ENVIRONMENT`. Tanto para entornos "local" como de "producción", utiliza el modelo `gpt-4o-mini`, enrutando a través de OpenRouter para "local" y directamente a OpenAI para "producción". Opcionalmente añade información de enrutamiento a la lista `updates["messages"]`. |