# RankPilot: Automatización Inteligente de Presentaciones Legales

RankPilot es un sistema sofisticado diseñado para automatizar y optimizar el proceso de creación, auditoría y presentación de información de bufetes de abogados a directorios prominentes como Legal500, Chambers y Leaders League. Aprovecha IA avanzada, incluyendo Modelos de Lenguaje Grandes (LLMs), para ingerir documentos, extraer y estructurar datos, identificar lagunas en las presentaciones, generar insights estratégicos y ensamblar documentos finales pulidos. El sistema tiene como objetivo reducir el esfuerzo manual, garantizar el cumplimiento de los requisitos del directorio y mejorar la calidad e impacto de las presentaciones de los bufetes de abogados.

## Introducción

Este documento sirve como una guía completa del código base de RankPilot. Describe la visión general del proyecto, la arquitectura, los componentes clave y proporciona orientación para comenzar. RankPilot representa un avance significativo en legal tech, simplificando un proceso complejo y que consume mucho tiempo en un flujo de trabajo eficiente impulsado por IA.

## Resumen del Proyecto

RankPilot automatiza el intrincado proceso de preparación y presentación de datos de bufetes de abogados a directorios de clasificación legal. Comienza ingiriendo diversos formatos de documentos (PDF, DOCX), clasificando su tipo y extrayendo texto relevante. Utilizando LLMs, luego estructura esta información según esquemas predefinidos para directorios como Legal500, Chambers y Leaders League. El sistema audita críticamente las presentaciones en busca de información faltante o "lagunas", interroga estratégicamente a los usuarios para obtener aclaraciones y optimiza el contenido para mayor claridad e impacto. Finalmente, genera resúmenes ejecutivos, hojas de ruta estratégicas y ensambla los documentos finales listos para presentar.

El núcleo de RankPilot se construye en torno a un flujo de trabajo agéntico orquestado por LangGraph, lo que permite un procesamiento modular y una adaptación dinámica a la entrada del usuario y a los problemas identificados. El sistema está diseñado para ser robusto, incorporando manejo de errores, saneamiento de datos y reintentos inteligentes.

## Arquitectura y Diseño

RankPilot emplea una arquitectura modular y basada en agentes, fuertemente influenciada por los patrones modernos de desarrollo de IA, particularmente LangGraph para orquestar flujos de trabajo complejos, secuenciales y condicionales.

*   **Flujo de Trabajo Agéntico:** El sistema está compuesto por numerosos "nodos de agente", cada uno responsable de una tarea específica dentro del proceso general de presentación (por ejemplo, clasificación, ingesta, auditoría, saneamiento, optimización, generación de estrategias). Estos agentes interactúan pasando un objeto `AgentState`, que encapsula el estado actual y los datos del trabajo de procesamiento.
*   **Orquestación de LangGraph:** LangGraph se utiliza para definir la máquina de estados que rige el flujo entre estos agentes. Esto permite el enrutamiento dinámico basado en la salida de los agentes anteriores, creando flujos de trabajo adaptables y resilientes. Las funciones clave de enrutamiento (`route_entry`, `route_after_audit`, `route_after_classification`) gestionan las transiciones entre diferentes etapas del proceso de presentación.
*   **Integración de LLM:** El uso extensivo de Modelos de Lenguaje Grandes (LLMs) es fundamental para la funcionalidad de RankPilot. Los LLMs se utilizan para:
    *   Clasificación de documentos.
    *   Extracción y estructuración de datos en esquemas Pydantic.
    *   Análisis de lagunas y generación de preguntas.
    *   Saneamiento y optimización de texto.
    *   Análisis estratégico, generación de resúmenes ejecutivos y creación de hojas de ruta.
    *   Se utilizan `langchain-openai` y bibliotecas relacionadas para las interacciones con LLMs, a menudo con analizadores de salida estructurada que aprovechan modelos Pydantic.
*   **Esquemas Pydantic:** Para una validación y serialización de datos robusta, se utilizan ampliamente los modelos Pydantic. Estos esquemas definen la estructura esperada para los datos de presentación en diferentes directorios (Legal500, Chambers, Leaders League), estados de agentes y pasos de procesamiento intermedios.
*   **Patrón de Estrategia:** Para manejar diferentes directorios legales y sus requisitos específicos, se implementa un patrón de estrategia. Módulos como `chambers`, `legal500` y `leaders_league` implementan cada uno una interfaz `SubmissionStrategy`, proporcionando métodos `audit` y `assemble` personalizados.
*   **Diseño Modular:** Los componentes se organizan en directorios lógicos (`agents`, `chains`, `core`, `io`, `logic`, `strategies`, `utils`). Esta modularidad promueve la reutilización, la mantenibilidad y la capacidad de prueba. Por ejemplo, las operaciones de entrada/salida están separadas en el módulo `io`, mientras que la lógica principal reside en `core`.
*   **Capa de API:** Una aplicación FastAPI (`main.py`) proporciona un punto de entrada de API para procesar solicitudes. Gestiona la cola de trabajos y el seguimiento del estado, lo que permite a sistemas externos o interfaces de usuario interactuar con el flujo de trabajo de RankPilot de forma asíncrona.
*   **Simulación y Pruebas:** Los scripts complementarios como `interactive_test.py` y `local_workflow_test.py` facilitan el desarrollo y las pruebas locales del flujo de trabajo, simulando interacciones de la interfaz de usuario y ejecución de extremo a extremo. También hay pruebas unitarias disponibles para varios módulos.

## Guía de Directorios

```
rankpilot-core/
├── agents/               # Contiene todos los módulos de agentes de IA responsables de tareas específicas.
│   ├── answer_evaluator.py
│   ├── assembler.py
│   ├── auditor.py
│   ├── chambers_ingestion.py
│   ├── classifier.py
│   ├── executive_writer.py
│   ├── extractor.py
│   ├── interrogator.py
│   ├── legal500_ingestion.py
│   ├── optimizer.py
│   ├── sanitizer.py
│   ├── scheduler.py
│   ├── snapshot_generator.py
│   ├── strategist.py
│   └── updater.py
├── chains/               # Alberga cadenas Langchain para procesos específicos impulsados por LLM.
│   ├── executive_writer_chain.py
│   ├── optimizer_chain.py
│   ├── scheduler_chain.py
│   └── snapshot_chain.py
├── configs/              # Archivos de configuración, probablemente incluyendo YAMLs para la configuración de estrategias.
├── core/                 # Utilidades principales y componentes fundamentales.
│   ├── engine.py
│   ├── llm.py
│   ├── schemas.py
│   ├── state.py
│   └── workflow.py
├── data/                 # Marcador de posición para archivos de datos (crudos, procesados).
│   ├── processed/
│   └── raw/
├── Documentation_set/    # Documentación relacionada con el proyecto.
├── src/                  # Directorio de código fuente, que refleja la estructura de nivel superior.
│   ├── agents/           # Implementación detallada de agentes.
│   ├── chains/           # Implementación detallada de cadenas.
│   ├── core/             # Implementación detallada de componentes principales.
│   ├── io/               # Utilidades de entrada/salida (manejo de archivos, codificación).
│   ├── logic/            # Lógica empresarial y generación de contexto.
│   └── strategies/       # Implementaciones de estrategias de presentación.
│       ├── base.py
│       ├── chambers.py
│       ├── leaders_league.py
│       └── legal500.py
├── templates/            # Plantillas de documentos utilizadas para el ensamblaje.
├── tests/                # Pruebas unitarias y de integración.
│   ├── test_io.py
│   ├── test_schemas.py
│   ├── test_strategies.py
│   ├── test_workflow.py
│   └── __init__.py
├── utils/                # Funciones de utilidad general.
├── interactive_test.py   # Script para pruebas interactivas del flujo de trabajo.
├── local_workflow_test.py # Script para pruebas locales de flujo de trabajo de extremo a extremo.
├── main.py               # Aplicación FastAPI para la API de RankPilot.
└── simulador_frontend.py # CLI que simula una interfaz de usuario que interactúa con la API.
```

## Tabla de Componentes

| Módulo                        | Responsabilidad                                                                         | Características Clave                                                                                                                                                                                                                             |
| :---------------------------- | :-------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agents/answer_evaluator.py`  | Procesa respuestas del usuario, determina la intención (completar, descartar, aclarar), actualiza la presentación. | Modelo Pydantic `AnswerIntent`, análisis de respuestas basado en LLM, actualizaciones anidadas de campos.                                                                                                                              |
| `agents/assembler.py`         | Orquesta el ensamblaje de documentos a partir de datos procesados.                      | Saneamiento de nombres de archivo, selección de estrategia para el ensamblaje, conversión de markdown a texto enriquecido, colocación del documento final.                                                                                       |
| `agents/auditor.py`           | Realiza análisis de lagunas frente a un esquema, teniendo en cuenta los campos descartados. | Compara los datos de presentación con el esquema ideal, identifica campos faltantes, incluye comprobaciones de plazos.                                                                                                                  |
| `agents/classifier.py`        | Clasifica tipos de documentos utilizando LLMs y carga configuraciones relevantes.       | Decodificación Base64, extracción de texto PDF/DOCX, clasificación de tipos de documentos basada en LLM, carga de configuración basada en la clasificación.                                                                                    |
| `agents/extractor.py`         | Ingiere y estructura el texto extraído en esquemas definidos utilizando LLMs.            | Fábrica de esquemas para diferentes tipos de presentación, LLM para extracción de datos estructurados, manejo de errores con respaldo de esquemas, inyección de metadatos.                                                              |
| `agents/executive_writer.py`  | Sintetiza datos en informes ejecutivos y cartas de auditoría.                          | Utiliza `executive_writer_chain`, prepara la entrada del LLM a partir del estado, procesa la salida del LLM para informes de alta autoridad.                                                                                                |
| `agents/interrogator.py`      | Genera preguntas estratégicas para llenar las lagunas de presentación identificadas.     | Esquema Pydantic `StrategicQuestion`, generación de preguntas impulsada por LLM basada en contexto y lagunas, preguntas dinámicas y contextualmente relevantes.                                                                          |
| `agents/optimizer.py`         | Refina y mejora el contenido de la presentación (narrativas, resaltados de trabajo).    | Utiliza `optimizer_chain`, aplica pautas de redacción publicitaria, optimiza en diferentes tipos de contenido (narrativas, asuntos, resúmenes).                                                                                               |
| `agents/sanitizer.py`         | Limpia y sanea los datos de texto en los objetos de presentación.                     | Identifica campos de cadenas largas, procesamiento por lotes con LLM para limpieza, modelos `CleanedField` y `SanitizationBatch`, recorrido recursivo de la estructura de datos.                                                               |
| `agents/scheduler.py`         | Genera un plan de acción estratégico (plan de 5 pasos) para los bufetes.               | Utiliza `scheduler_chain`, extrae datos estratégicos del estado, formatea la entrada del LLM, genera `evolution_path` y `current_step`.                                                                                                  |
| `agents/snapshot_generator.py`| Genera una instantánea estratégica final y una clasificación arquetípica.              | Orquesta `archetype_chain` y `snapshot_chain`, procesa los datos del estado para su análisis, genera instantánea de evaluación estructurada.                                                                                                |
| `agents/strategist.py`        | Genera planes de acción estratégicos y resúmenes ejecutivos a partir de texto crudo y lagunas. | Emplea LLM para salida estructurada, crea modelos `MilestoneSchema` y `StrategistResponse`, sintetiza planes de acción.                                                                                                                         |
| `agents/updater.py`           | Procesa respuestas del usuario para actualizar los datos de presentación a través de `SubmissionPatch`. | Esquemas Pydantic `FieldUpdate` y `SubmissionPatch`, LLM para traducción y estructuración de respuestas, `deep_update_field` para fusionar actualizaciones.                                                                                 |
| `chains/`                     | Cadenas Langchain para tareas específicas impulsadas por LLM.                          | Encapsula prompts, LLMs y analizadores de salida para tareas complejas de generación y estructuración de texto (por ejemplo, redacción ejecutiva, optimización, programación, creación de instantáneas).                                       |
| `core/llm.py`                 | Fábrica para crear instancias de LLM configuradas.                                      | Soporta OpenAI y OpenRouter, configuraciones específicas del entorno, registro opcional de mensajes de diagnóstico.                                                                                                                   |
| `core/schemas.py`             | Modelos Pydantic para estructurar los datos de presentación para diferentes directorios. | Esquemas completos para presentaciones de Legal500, Chambers, Leaders League, incluyendo identidad, departamentos, clientes, asuntos, comentarios, etc.                                                                                      |
| `core/state.py`               | Define el modelo `AgentState` y estructuras de datos relacionadas.                    | Gestión de estado centralizada, utilidades de saneamiento (`sanitize_nulls_from_php`, `normalize_submission_type`, `sanitize_php_garbage`), manejo de respuestas del usuario (`sanitize_new_answer`).                                          |
| `core/workflow.py`            | Define el flujo de trabajo principal de LangGraph para el procesamiento de documentos.    | Definición de máquina de estados (`StateGraph`), orquestación de nodos de agente (Actos I, II, III), lógica de enrutamiento para la progresión dinámica del flujo de trabajo.                                                                  |
| `io/`                         | Utilidades de entrada/salida.                                                           | Codificación/decodificación Base64, análisis de DOCX y PDF, enriquecimiento de texto, utilidades de selección de estrategia.                                                                                                           |
| `logic/`                      | Lógica empresarial, generación de contexto y definiciones de reglas.                    | Contextos específicos de bufetes, contextos de mercado, reglas de inteligencia de prácticas, análisis de historial de clasificación, objetivos estratégicos.                                                                                     |
| `strategies/`                 | Implementaciones de estrategias de presentación específicas.                          | Subclases `Legal500Strategy`, `ChambersStrategy`, `LeadersLeagueStrategy` que proporcionan métodos `audit` y `assemble` basados en configuraciones YAML específicas del directorio.                                                               |
| `templates/`                  | Plantillas DOCX para generar documentos de presentación finales.                      | Marcador de posición para archivos de plantilla utilizados por `docxtpl` durante el proceso de ensamblaje.                                                                                                                             |
| `interactive_test.py`         | Simula una interfaz de usuario sin estado para probar la API de backend.              | Simulación de carga de PDF, codificación Base64, respuesta iterativa a preguntas del backend, solicitudes HTTP POST a la API.                                                                                                           |
| `local_workflow_test.py`      | Orquesta la ejecución del flujo de trabajo de extremo a extremo en un entorno de prueba local. | Simula la presentación del usuario (documento/texto), gestión de estado, llenado interactivo de lagunas, salida de diagnóstico, guardado del documento final.                                                                              |
| `main.py`                     | Aplicación FastAPI que sirve como API de RankPilot.                                     | Puntos de entrada de API para procesamiento de documentos (`/process`) y sondeo de estado (`/status/{job_id}`), gestión de tareas en segundo plano para la ejecución del flujo de trabajo, simulación de base de datos de trabajos (`JOBS_DB`). |
| `simulador_frontend.py`       | Interfaz de línea de comandos (CLI) que simula la interfaz de RankPilot.          | Opciones de entrada del usuario (carga, texto crudo, lienzo en blanco), sondeo de la API del backend para obtener el estado, visualización del progreso y resultados, simulación de interacciones de análisis estratégico.                 |

## Comenzar

Para comenzar con RankPilot, siga estos pasos generales:

1.  **Prerrequisitos:**
    *   Python 3.9+
    *   Administrador de paquetes `pip`

2.  **Clonar el Repositorio:**
    ```bash
    git clone <repository_url>
    cd rankpilot-core
    ```

3.  **Configurar un Entorno Virtual:**
    Se recomienda encarecidamente utilizar un entorno virtual para gestionar las dependencias del proyecto.
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows use `venv\Scripts\activate`
    ```

4.  **Instalar Dependencias:**
    Instale todos los paquetes de Python requeridos.
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Si `requirements.txt` no se proporciona explícitamente, normalmente instalaría los paquetes enumerados en los resúmenes de módulos o inferidos de las importaciones).*

5.  **Variables de Entorno:**
    Asegúrese de que las variables de entorno necesarias estén configuradas, particularmente para las claves de API (por ejemplo, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`) y potencialmente para la configuración del entorno (`ENVIRONMENT`). Consulte `.env.example` si está disponible para obtener orientación.

6.  **Ejecutar la Interfaz de Usuario Simulado/API:**
    *   **Para ejecutar el backend FastAPI:**
        ```bash
        uvicorn main:app --reload
        ```
    *   **Para ejecutar la prueba de flujo de trabajo local:**
        ```bash
        python local_workflow_test.py
        ```
    *   **Para ejecutar la prueba interactiva (simulando llamadas a la API de la interfaz de usuario):**
        ```bash
        python interactive_test.py --filepath /path/to/your/document.pdf
        ```
    *   **Para ejecutar el simulador CLI:**
        ```bash
        python simulador_frontend.py
        ```

7.  **Configuración:**
    *   Revise y ajuste los archivos de configuración en el directorio `configs/` según sea necesario, especialmente para diferentes directorios legales.
    *   Asegúrese de que las claves de API y otra información sensible se gestionen de forma segura.

Esta configuración proporciona una base para ejecutar las funcionalidades principales de RankPilot, probar flujos de trabajo e interactuar con el sistema. Para casos de uso específicos o desarrollo más allá de estos conceptos básicos, consulte la documentación de módulos individuales y el directorio `Documentation_set`.