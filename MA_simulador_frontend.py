import requests
import time
import uuid
import base64
import os

# URL base donde corre nuestro backend FastAPI
BASE_URL = "http://127.0.0.1:8000"

def remove_none_values(obj):
    """
    Recursively removes keys with None values to prevent Pydantic validation crashes.
    """
    if isinstance(obj, dict):
        return {k: remove_none_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_none_values(v) for v in obj if v is not None]
    return obj

def print_header(texto):
    print(f"\n{'='*50}\n{texto}\n{'='*50}")

# 🛡️ THE FRONTEND SANITIZER
def to_dict(obj):
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return {}

def get_mime_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.pdf': return "application/pdf"
    elif ext in ['.docx', '.doc']: return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif ext in ['.jpg', '.jpeg']: return "image/jpeg"
    elif ext == '.png': return "image/png"
    elif ext == '.txt': return "text/plain"
    return "application/octet-stream"

def main():
    print_header("🚀 MATTERS ASSISTANT SIMULATOR (ACT 0)")
    print("Este módulo crea UN (1) Matter perfecto a partir de datos desestructurados.")
    
    base64_docs = []
    raw_text = ""
    
    print("\n[Fase 1: Ingesta Multimodal]")
    print("Puedes subir hasta 10 archivos (PDF, DOCX, JPG, PNG, TXT).")
    print("Escribe 'listo' cuando hayas terminado de agregar archivos.")
    
    while len(base64_docs) < 10:
        ruta = input(f"[{len(base64_docs)+1}/10] Ruta del archivo (o 'listo'): ").strip('"').strip("'")
        
        if ruta.lower() == 'listo':
            break
            
        if os.path.exists(ruta):
            try:
                mime_type = get_mime_type(ruta)
                with open(ruta, "rb") as archivo:
                    contenido_binario = archivo.read()
                
                base64_string = base64.b64encode(contenido_binario).decode('utf-8')
                nombre_archivo = os.path.basename(ruta)
                
                base64_docs.append({
                    "filename": nombre_archivo,
                    "mime_type": mime_type,
                    "base64_data": base64_string,
                    "base64": base64_string 
                })
                print(f"✅ Archivo '{nombre_archivo}' ({mime_type}) cargado exitosamente.")
                
            except Exception as e:
                print(f"❌ Error al leer o convertir el archivo: {e}")
        else:
            print(f"❌ Error: No se encontró el archivo: {ruta}")
            
    if len(base64_docs) == 10:
        print("⚠️ Límite de 10 archivos alcanzado.")

    print("\n[Fase 2: Notas del Abogado]")
    raw_text = input("Pega correos reenviados o notas crudas aquí (Presiona Enter para omitir):\n> ")

    if not base64_docs and not raw_text.strip():
        print("❌ No enviaste datos. Saliendo del simulador...")
        return

    # 1. ESTADO INICIAL PARA ACTO 0
    thread_id = str(uuid.uuid4())
    agent_state = {
        "metadata": {
            "firm_name": "", 
            "practice_area": "", 
            "directory": "Chambers",
            "guide": "Matters Assistant",
            "submission_deadline": "December 25 2026",
            "jurisdiction": "", 
        },
        "target_submission_type": "MattersAssistant", 
        "input_document_type": "raw_batch", 
        "base64_documents": base64_docs,
        "raw_text": raw_text,
        "raw_input_text": raw_text,
        # 🛡️ THE FIX: Start with the correct dictionary structure
        "submission": {"matter": {}}, 
        "gaps": []
    }

    # 2. ENVIAR PETICIÓN
    print("\n📡 Encendiendo la forja (Genesis Drafter)...")
    payload = {
        "thread_id": thread_id,
        "agent_state": agent_state
    }

    print(f"agent state submissions: {agent_state.get('submission')}")
    
    response = requests.post(f"{BASE_URL}/process", json=payload)
    if response.status_code != 200:
        print("❌ Error del servidor:", response.text)
        return
        
    current_job_id = response.json()["job_id"]
    
    # 3. CICLO DE POLLING Y AUDITORÍA
    while True:
        print("\n⏳ Procesando...")
        
        while True:
            status_response = requests.get(f"{BASE_URL}/status/{current_job_id}")
            if status_response.status_code != 200:
                print("\n❌ Error de conexión con el servidor.")
                return
                
            status_data = status_response.json()
            
            if status_data["status"] in ["started", "processing"]:
                progreso = status_data.get('progress', 0)
                barra = "█" * (progreso // 5) + "-" * (20 - (progreso // 5))
                print(f"\r[{barra}] {progreso}% - {status_data.get('message', '')}", end="", flush=True)
                time.sleep(2)
                
            elif status_data["status"] == "completed":
                print(f"\n\n[{'█'*20}] 100% - ¡Extracción Completada!")
                break 
            
            elif status_data["status"] == "failed":
                print("\n\n❌ EL TRABAJO FALLÓ EN EL SERVIDOR.")
                print(f"Detalles: {status_data.get('error_details', status_data.get('message'))}")
                break
        
        if status_data["status"] == "failed":
            break
            
        ia_data = status_data.get("data", {})
        if not ia_data:
            print("\n⚠️ Advertencia: No se recibió data procesada.")
            break

        # =======================================================
        # 🧠 THE MEMORY SYNC FIX (EXPLICIT OVERWRITE)
        # =======================================================
        meta_recibida = to_dict(ia_data.get("metadata", {}))
        
        # Merge incoming metadata carefully so we never lose the deadline
        if meta_recibida:
            if "metadata" not in agent_state:
                agent_state["metadata"] = {}
            agent_state["metadata"].update(meta_recibida)

        for key, value in ia_data.items():
            if key == "metadata": 
                continue 
                
            if value is not None:
                if isinstance(value, list):
                    agent_state[key] = [to_dict(v) if hasattr(v, '__dict__') or hasattr(v, 'model_dump') else v for v in value]
                elif hasattr(value, '__dict__') or hasattr(value, 'model_dump'):
                    agent_state[key] = to_dict(value)
                else:
                    agent_state[key] = value
                
        gaps = agent_state.get("gaps", [])
        
        # CONDICIÓN DE SALIDA: Si ya no hay brechas que el auditor detecte
        if not gaps:
            print_header("🎯 MATTER GENERADO CON ÉXITO")
            
            submission_data = to_dict(ia_data.get("submission", {}))
            matter = submission_data.get("matter", {})
            
            if not matter:
                print("⚠️ No se encontró la estructura 'matter' en la respuesta.")
                break
                
            print(f" 🏢 Cliente       : {matter.get('client_name', 'No especificado')}")
            print(f" 🏷️  Título        : {matter.get('matter_title', 'No especificado')}")
            print(f" 💰 Valor         : {matter.get('matter_value', 'No especificado')}")
            print(f" 📅 Status/Fecha  : {matter.get('date_completion_or_status', 'No especificado')}")
            print(f" 🔒 Confidencial  : {'SÍ' if matter.get('is_confidential') else 'NO'}")
            
            print("\n 🧑‍⚖️  Socios Líderes :", ", ".join(matter.get("lead_partners", [])))
            print(" 👥  Equipo         :", ", ".join(matter.get("other_team_members", [])))
            print(" 🌍  Cross-Border   :", ", ".join(matter.get("cross_border_jurisdictions", [])))
            print(" 🤝  Otras Firmas   :", ", ".join(matter.get("other_firms_advising", [])))
            
            print("\n 📝 RESUMEN (Magic Circle Tone):")
            print("-" * 50)
            print(matter.get("summary_of_matter_and_role", "Sin resumen."))
            print("-" * 50)
            
            print("\n✅ ¡Listo para ser inyectado en el docx principal!")
            break
            
        # =======================================================
        # CHAT DE AUDITORÍA (THE INTERROGATOR)
        # =======================================================
        print_header(f"🛑 EL AUDITOR REQUIERE INFORMACIÓN: Faltan {len(gaps)} campos obligatorios")
        
        preguntas = ia_data.get("questions", [])
        pregunta = preguntas[0] if preguntas else "¿Puedes proporcionar la información faltante?"
        print(f"🤖 IA: {pregunta}")
        
        respuesta_usuario = input("\n👤 Tu respuesta: ")
        
        gap_actual = gaps[0]["field"] if gaps else "general"
        
        # =======================================================
        # 🛡️ THE METADATA SANITIZER (Mirrored from Normal Simulator)
        # Prevent Pydantic from crashing on empty file_base64 objects
        # =======================================================
        if "metadata" in agent_state:
            bad_file_data = agent_state["metadata"].get("file_base64")
            if bad_file_data == "" or bad_file_data is None:
                del agent_state["metadata"]["file_base64"]
                
        # Limpiamos questions para evitar el error de Pydantic [List[str]]
        agent_state["questions"] = []
        
        # =======================================================
        # 🧹 🛡️ SANITIZE SUBMISSION
        # Remove explicit Nones so main.py doesn't crash and wipe it
        # =======================================================
        agent_state["submission"] = remove_none_values(agent_state.get("submission", {}))
        
        # Build the answer payload
        agent_state["new_answer"] = {
            "target_field": gap_actual,
            "question_text": pregunta,
            "answer": respuesta_usuario
        }
        
        payload_respuesta = {
            "thread_id": thread_id,
            "agent_state": agent_state
        }

        print(f"submission data before sending answer: {agent_state.get('submission')}")
        
        print("\n📡 Inyectando datos y reanudando la extracción...")
        resp = requests.post(f"{BASE_URL}/process", json=payload_respuesta)
        if resp.status_code != 200:
             print("❌ Error al enviar la respuesta:", resp.text)
             break
             
        current_job_id = resp.json().get("job_id")

if __name__ == "__main__":
    main()