1. ## Resumen:
Este archivo contiene una función para analizar un diccionario de envío e identificar contextos estratégicos específicos de la firma basándose en reglas predefinidas relacionadas con contrataciones/salidas importantes y actividad transfronteriza.

2. ## Clases:
Ninguna

3. ## Funciones y Métodos:

| Nombre | Parámetros | Responsabilidad |
|---|---|---|
| `get_firm_specific_context` | `submission_dict: Dict[str, Any]`, `directory_type: str` | Analiza el `submission_dict` para detectar cambios sísmicos (contrataciones/salidas) y huella transfronteriza. Devuelve una cadena que resume los contextos detectados, o un mensaje predeterminado si no se encuentran contextos específicos. |