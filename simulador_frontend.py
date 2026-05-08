import requests
import time
import uuid
import base64
import os

# URL base donde corre nuestro simulador FastAPI
BASE_URL = "http://127.0.0.1:8000"

def print_header(texto):
    print(f"\n{'='*50}\n{texto}\n{'='*50}")

def main():
    print_header("🚀 RANKPILOT FRONTEND SIMULATOR (CLI)")
    print("Selecciona tu vía de entrada:")
    print("1. 📄 Upload Draft (.docx / .pdf)")
    print("2. ✍️ Paste Raw Text")
    print("3. ✨ Start from Scratch")
    
    opcion = input("\nElige una opción (1/2/3): ")
    
    input_type = "scratch"
    base64_docs = []
    raw_text = ""
    
    if opcion == "1":
        input_type = "docx"
        print("\n[Simulador de Carga de Archivos]")
        ruta_archivo = input("📁 Arrastra o pega la ruta completa de tu archivo: ").strip('"').strip("'")
        
        if os.path.exists(ruta_archivo):
            try:
                with open(ruta_archivo, "rb") as archivo:
                    contenido_binario = archivo.read()
                
                base64_string = base64.b64encode(contenido_binario).decode('utf-8')
                nombre_archivo = os.path.basename(ruta_archivo)
                
                base64_docs = [{"filename": nombre_archivo, "base64": base64_string}]
                print(f"✅ Archivo '{nombre_archivo}' cargado exitosamente.")
                
            except Exception as e:
                print(f"❌ Error al leer o convertir el archivo: {e}")
                return
        else:
            print(f"❌ Error: No se encontró ningún archivo en la ruta: {ruta_archivo}")
            return
    elif opcion == "2":
        input_type = "raw_text"
        raw_text = input("\nPega tu texto crudo aquí: ")
    elif opcion == "3":
        input_type = "scratch"
        print("\n[Iniciando lienzo en blanco...]")
    else:
        print("Opción no válida. Saliendo...")
        return

    # 1. ESTADO INICIAL
    thread_id = str(uuid.uuid4())
    agent_state = {
        "metadata": {
            "firm_name": "",  # <--- ¡Añade esto!
            "directory": "Chambers",
            "guide": "USA", 
            "practice_area": "Fintech",
            "jurisdiction": ""             
        },
        "target_submission_type": "Chambers",
        "input_document_type": input_type,
        "base64_documents": base64_docs,
        "raw_input_text": raw_text,
        "submission": {},
        "gaps": []
    }

    # 2. ENVIAR PETICIÓN INICIAL
    print("\n📡 Iniciando motor RankPilot...")
    payload = {
        "thread_id": thread_id,
        "agent_state": agent_state
    }
    
    response = requests.post(f"{BASE_URL}/process", json=payload)
    if response.status_code != 200:
        print("❌ Error del servidor:", response.text)
        return
        
    current_job_id = response.json()["job_id"]
    
    # 3. CICLO INFINITO DE LA APLICACIÓN
    while True:
        print("\n⏳ Procesando...")
        
        # --- Bucle de Polling Limpio ---
        while True:
            status_response = requests.get(f"{BASE_URL}/status/{current_job_id}")
            if status_response.status_code != 200:
                print("\n❌ Error de conexión con el servidor.")
                return
                
            status_data = status_response.json()
            
            if status_data["status"] in ["started", "processing"]:
                progreso = status_data.get('progress', 0)
                barra = "█" * (progreso // 5) + "-" * (20 - (progreso // 5))
                # Animación en una sola línea
                print(f"\r[{barra}] {progreso}% - {status_data.get('message', '')}", end="", flush=True)
                time.sleep(2)
                
            elif status_data["status"] == "completed":
                print(f"\n\n[{'█'*20}] 100% - ¡Proceso Completado!")
                break 
            
            elif status_data["status"] == "failed":
                print("\n\n❌ EL TRABAJO FALLÓ EN EL SERVIDOR.")
                print(f"Detalles: {status_data.get('error_details', status_data.get('message'))}")
                break
        
        if status_data["status"] == "failed":
            break
            
        # --- Evaluación del Resultado ---
        ia_data = status_data.get("data", {})
        if not ia_data:
            print("\n⚠️ Advertencia: No se recibió data procesada.")
            break
            
        # 🕵️‍♂️ NUEVO: BLOQUE DE DEBUG DE METADATA
        print_header("🔍 DEBUG: METADATA RECIBIDA DEL SERVIDOR")
        meta_recibida = ia_data.get("metadata", {})
        print(f"Firma         : {meta_recibida.get('firm_name', 'Vacío')}")
        print(f"Directorio    : {meta_recibida.get('directory', 'Vacío')}")
        print(f"Guía          : {meta_recibida.get('guide', 'Vacío')}")
        print(f"Área          : {meta_recibida.get('practice_area', 'Vacío')}")
        print("="*50)
            
        for key, value in ia_data.items():
            if value is not None:
                agent_state[key] = value
                
        gaps = agent_state.get("gaps", [])
        
        # CONDICIÓN DE SALIDA
        # CONDICIÓN DE SALIDA: Cuando ya no hay más preguntas (gaps)
        if not gaps:
            # 1. Función para normalizar cualquier dato (Pydantic o Dict) a Dict
            def to_dict(obj):
                if isinstance(obj, dict):
                    return obj
                if hasattr(obj, "model_dump"): # Si es Pydantic v2
                    return obj.model_dump()
                if hasattr(obj, "__dict__"): # Fallback para objetos genéricos
                    return obj.__dict__
                return {}

            # 2. Extraer y normalizar los bloques clave del estado
            p_core = to_dict(ia_data.get("positioning_core", {}))
            p_tier = to_dict(ia_data.get("positioning_tier", {}))
            s_context = to_dict(ia_data.get("strategic_context", {}))

            # 3. IMPRESIÓN DE CASILLAS ESTRATÉGICAS[cite: 3]
            print_header("🏆 DIAGNÓSTICO ESTRATÉGICO FINAL")
            
            # Ahora usamos .get() con total seguridad porque todo es un dict
            print(f" { 'ARQUETIPO':<20} : {p_core.get('practice_model', 'N/A')}")
            print(f" { 'TIER DETECTADO':<20} : {p_tier.get('label', 'N/A')}")
            print(f" { 'TARGET':<20} : {s_context.get('realistic_target', 'N/A')}")
            
            # Cálculo de confianza con fallback seguro
            conf = p_core.get('confidence_score', 0)
            print(f" { 'CONFIANZA':<20} : {float(conf) * 100}%")
            
            print_header("🎨 ESTRATEGIA DE NARRATIVA (MAQUILLAJE)")
            guidelines = p_core.get("narrative_guidelines", "No guidelines generated.")
            if isinstance(guidelines, list):
                for g in guidelines: print(f" • {g}")
            else:
                print(guidelines)

            print_header("⚖️ JUSTIFICACIÓN DEL TIER")
            print(p_tier.get("explanation", "Sin justificación disponible."))

            print_header("🕵️‍♂️ SEÑALES DE MERCADO DETECTADAS")
            signals = p_core.get("signals", [])
            if signals and isinstance(signals, list):
                for s in signals: print(f" 🚩 {s}")
            else:
                print("No se detectaron señales de respaldo.")

            print_header("📅 ROADMAP DE EVOLUCIÓN")
            # El roadmap ya suele venir como lista de dicts por el model_dump del nodo[cite: 9]
            roadmap = ia_data.get("evolution_path", [])
            for step in roadmap:
                s = to_dict(step)
                print(f" [{s.get('target_completion_date', 'TBD')}] {s.get('action_title', 'ACCIÓN').upper()}")

            # --- NUEVA SECCIÓN: EXECUTIVE WRITER FINAL ANALYSIS ---
            print_header("📝 REPORTE FINAL DEL EXECUTIVE WRITER")
            exec_summary = to_dict(ia_data.get("executive_summary", {}))
            
            if exec_summary:
                score = exec_summary.get('overall_score', 'N/A')
                risk = exec_summary.get('risk_level', 'N/A')
                
                print(f" 📊 SCORE GLOBAL   : {score}/100")
                print(f" ⚠️ NIVEL DE RIESGO: {risk.upper() if isinstance(risk, str) else risk}")
                print(f"\n 💡 VEREDICTO ESTRATÉGICO:\n {exec_summary.get('strategic_verdict', 'Sin veredicto.')}")
                
                diffs = exec_summary.get('top_differentiators', [])
                if diffs and isinstance(diffs, list):
                    print("\n 🎯 TOP DIFERENCIADORES A EXPLOTAR:")
                    for d in diffs:
                        print(f"   • {d}")
                
                letter = exec_summary.get('audit_letter_markdown', '')
                if letter:
                    print_header("✉️ CARTA DE AUDITORÍA AL DIRECTORIO")
                    print(letter)
                else:
                    print("\n⚠️ La carta de auditoría no se generó o está vacía.")
            else:
                print("⚠️ No se encontró el bloque 'executive_summary' en el estado final.")

            print_header("✨ PROCESO COMPLETADO")
            break
            
        # CHAT DE AUDITORÍA
        print_header(f"🛑 AUDIT ROOM: {len(gaps)} brechas estratégicas detectadas")
        
        preguntas = ia_data.get("questions", [])
        pregunta = preguntas[0] if preguntas else "¿Puedes proporcionar más detalles sobre esto?"
        print(f"🤖 IA: {pregunta}")
        
        respuesta_usuario = input("\n👤 Tu respuesta: ")
        
        gap_actual = gaps[0]["field"] if gaps else "general"
        
        agent_state["new_answer"] = {
            "target_field": gap_actual,
            "question_text": pregunta,
            "answer": respuesta_usuario
        }
        
        payload_respuesta = {
            "thread_id": thread_id,
            "agent_state": agent_state
        }
        
        print("\n📡 Analizando nueva información...")
        resp = requests.post(f"{BASE_URL}/process", json=payload_respuesta)
        
        if resp.status_code != 200:
             print("❌ Error al enviar la respuesta:", resp.text)
             break
             
        current_job_id = resp.json().get("job_id")

if __name__ == "__main__":
    main()