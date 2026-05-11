# Resumen:
Este archivo contiene pruebas unitarias para las clases `Legal500Strategy` y `ChambersStrategy`. Verifica su inicialización, carga de configuración y funcionalidad de auditoría básica.

# Clases:
- `TestStrategies`: Una clase de prueba que hereda de `unittest.TestCase` para agrupar las pruebas relacionadas con las estrategias.

# Funciones y Métodos:
| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `test_legal500_strategy_init` | `self` | Prueba la inicialización de `Legal500Strategy`, verifica la presencia de `config`, valida el atributo 'name' en la configuración y confirma que el método `audit` devuelve una lista no vacía de huecos. |
| `test_chambers_strategy_init` | `self` | Prueba la inicialización de `ChambersStrategy`, verifica la presencia de `config`, valida el atributo 'name' en la configuración y confirma que el método `audit` devuelve una lista no vacía de huecos. |