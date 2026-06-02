import requests
import time
import uuid
import base64
import os

# URL base donde corre nuestro simulador FastAPI
BASE_URL = "http://127.0.0.1:8000"

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
            "firm_name": "", 
            "directory": "Chambers",
            "guide": "USA", 
            "practice_area": "Fintech",
            "submission_deadline": "December 25 2026",
            "jurisdiction": "Mexico",
            "current_band": "Unranked",
        },
        "target_submission_type": "Chambers",
        "input_document_type": input_type,
        "base64_documents": base64_docs,
        "raw_text": raw_text,
        "submission": {},
        "strategic_context": {}, 
        "gaps": [],
        "lawyer_profiles": [],
        "positioning_core": {},
        "positioning_tier": {},
        "executive_summary": {}
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
    
    has_entered_audit_room = False
    active_category = None
    forced_generation = False
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
            
        ia_data = status_data.get("data", {})
        if not ia_data:
            print("\n⚠️ Advertencia: No se recibió data procesada.")
            break
        
        # 🕵️‍♂️ BLOQUE DE DEBUG DE METADATA
        print_header("🔍 DEBUG: METADATA RECIBIDA DEL SERVIDOR")
        meta_recibida = to_dict(ia_data.get("metadata", {}))
        print(f"Firma         : {meta_recibida.get('firm_name', 'Vacío')}")
        print(f"Directorio    : {meta_recibida.get('directory', 'Vacío')}")
        print(f"Guía          : {meta_recibida.get('guide', 'Vacío')}")
        print(f"Área          : {meta_recibida.get('practice_area', 'Vacío')}")
        print(f"Deadline      : {meta_recibida.get('submission_deadline', 'No establecido')}")
        print("="*50)
            
        # =======================================================
        # 🧠 THE MEMORY SYNC FIX (EXPLICIT OVERWRITE)
        # =======================================================
        if meta_recibida:
            agent_state["metadata"] = meta_recibida

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
        
        # CONDICIÓN DE SALIDA: Cuando ya no hay más preguntas (gaps)
        if not gaps or forced_generation:

            p_core = to_dict(ia_data.get("positioning_core", {}))
            p_tier = to_dict(ia_data.get("positioning_tier", {}))
            s_context = to_dict(ia_data.get("strategic_context", {}))

            print_header("🏆 DIAGNÓSTICO ESTRATÉGICO FINAL")
            print(f" { 'ARQUETIPO':<20} : {p_core.get('practice_model', 'N/A')}")
            print(f" { 'TIER DETECTADO':<20} : {p_tier.get('label', 'N/A')}")
            print(f" { 'TARGET':<20} : {s_context.get('realistic_target', 'N/A')}")
            
            conf = p_core.get('confidence_score', 0)
            print(f" { 'CONFIANZA':<20} : {float(conf)}%")
            
            print_header("🎨 ESTRATEGIA DE NARRATIVA (MAQUILLAJE)")
            guidelines = p_core.get("narrative_guidelines", "No guidelines generated.")
            if isinstance(guidelines, list):
                for g in guidelines: print(f" • {g}")
            else:
                print(guidelines)

            print_header("📝 REPORTE FINAL DEL EXECUTIVE WRITER")
            exec_summary = to_dict(ia_data.get("executive_summary", {}))
            
            if exec_summary:
                score = exec_summary.get('overall_score', 'N/A')
                risk = exec_summary.get('risk_level', 'N/A')
                
                print(f" 📊 SCORE GLOBAL   : {score}/100")
                print(f" ⚠️ NIVEL DE RIESGO: {risk.upper() if isinstance(risk, str) else risk}")
                print(f"\n 💡 VEREDICTO ESTRATÉGICO:\n {exec_summary.get('strategic_verdict', 'Sin veredicto.')}")
            else:
                print("⚠️ No se encontró el bloque 'executive_summary' en el estado final.")

            print_header("💼 ANÁLISIS ESTRATÉGICO DE CASOS (MATTERS)")
            submission_data = to_dict(ia_data.get("submission", {}))
            
            def print_matter_evaluation(m_dict, index):
                client = m_dict.get("D1_name_of_client", m_dict.get("E1_name_of_client", "Unknown Client"))
                val = m_dict.get("D3_matter_value", m_dict.get("E3_matter_value", "N/A"))
                print(f"\n  [{index}] Cliente: {client} | Valor: {val}")

                evaluation = m_dict.get("evaluation", {})
                if evaluation:
                    total_score = evaluation.get("total_score", "N/A")
                    label = evaluation.get("classification_label", "Unclassified")
                    print(f"      🎯 Rúbrica   : {total_score}/100 | {label.upper()}")

            pub_info = submission_data.get("D_publishable_information", {})
            pub_matters = pub_info.get("publishable_matters", []) if pub_info else []
            conf_info = submission_data.get("E_confidential_information", {})
            conf_matters = conf_info.get("confidential_matters", []) if conf_info else []

            max_to_print = 3 
            printed_count = 0

            if pub_matters:
                for i, m in enumerate(pub_matters):
                    if printed_count >= max_to_print: break
                    print_matter_evaluation(to_dict(m), i+1)
                    printed_count += 1

            print_header("⚖️ EVALUACIÓN DE BENCH STRENGTH (ABOGADOS)")
            raw_profiles = agent_state.get("lawyer_profiles", [])
            lawyer_profiles = [to_dict(lp) for lp in raw_profiles] if raw_profiles else []
            
            if lawyer_profiles:
                for i, lawyer in enumerate(lawyer_profiles):
                    name = lawyer.get("name", "Desconocido")
                    role = "Socio" if lawyer.get("is_partner") else "Asociado/Counsel"
                    target = lawyer.get("target_ranking", "No especificado")
                    
                    print(f"\n  [{i+1}] 🧑‍⚖️ {name} ({role}) | Target: {target}")
                    
                    rubric = lawyer.get("rubric_evaluation", {})
                    if rubric:
                        score = rubric.get("total_readiness_score", "N/A")
                        print(f"      🎯 Puntuación de Evidencia : {score}/110")
                        
                    diagnosis = lawyer.get("executive_diagnosis", {})
                    if diagnosis:
                        action = diagnosis.get("recommended_action", "N/A")
                        rationale = diagnosis.get("rationale", "N/A")
                        print(f"      📈 Acción Recomendada      : {action}")
                        print(f"      💡 Justificación           : {rationale}")
                    
                    opt_bio = lawyer.get("optimized_biography", "")
                    if opt_bio:
                        print(f"      ✍️ Bio Optimizada (Ghostwritten):")
                        print(f"         \"{opt_bio[:300]}...\"")
            else:
                print("⚠️ No se extrajeron o evaluaron perfiles de abogados en este ciclo.")

            print_header("✨ PROCESO COMPLETADO")
            break
            
        # =======================================================
        # 🎨 SIMULAR VIEW 1: CONTEXTO INICIAL (DASHBOARD)
        # =======================================================
        print_header(f"🛑 AUDIT ROOM: {len(gaps)} brechas estratégicas detectadas")
        
        ui_snapshot = ia_data.get("ui_context_snapshot", {})
        audit_options = ui_snapshot.get("audit_room_options", []) if ui_snapshot else []
        
        if ui_snapshot and audit_options and not has_entered_audit_room:
            print_header("✨ VIEW 1: CONTEXTO INICIAL (DASHBOARD) ✨")
            print(f" 🏢 Firma       : {ui_snapshot.get('firm_name', 'Unknown')}")
            print(f" 📈 Trayectoria : {ui_snapshot.get('current_band', '?')} -> {ui_snapshot.get('target_band', '?')}")
            print(f" 💼 Matters     : {ui_snapshot.get('matters_count', 0)}")
            print(f" 🧑‍⚖️ Lawyers     : {ui_snapshot.get('lawyers_count', 0)}")
            print(f" 🎯 Confianza   : {ui_snapshot.get('initial_confidence', 0.0)}%")
            print("-" * 50)
            print("¿Qué te gustaría reforzar? (Simulando clicks de Laravel)")
            
            for i, opt in enumerate(audit_options):
                count = opt.get('count', 0)
                print(f"  [{i+1}] {opt.get('title', 'Option')} ({count} questions) - {opt.get('subtitle', '')}")
            
            print("\n  [0] Ingresar al Audit Room normalmente (Pregunta por defecto)")
            print("  [99] 🚀 Generar Documento (Omitir brechas restantes y compilar)")
            
            choice = input("\n👉 Elige una opción: ").strip()
            
            has_entered_audit_room = True 

            if choice == "99":
                print("\n🚀 Iniciando fase de Ghostwriting y Ensamblaje...")
                forced_generation = True  
                agent_state["new_answer"] = {
                    "target_field": "COMMAND:GENERATE",
                    "question_text": "",
                    "answer": ""
                }
                if "strategic_context" not in agent_state:
                    agent_state["strategic_context"] = {}
                agent_state["strategic_context"]["active_category"] = active_category
                
                payload_respuesta = {
                    "thread_id": thread_id,
                    "agent_state": agent_state
                }
                payload_respuesta = {"thread_id": thread_id, "agent_state": agent_state}
                resp = requests.post(f"{BASE_URL}/process", json=payload_respuesta)
                if resp.status_code != 200:
                    print("❌ Error al enviar la señal:", resp.text)
                    break
                current_job_id = resp.json().get("job_id")
                has_entered_audit_room = False 
                active_category = None
                continue
            
            if choice.isdigit() and int(choice) > 0 and int(choice) <= len(audit_options):
                selected_opt = audit_options[int(choice)-1]
                print(f"\n📡 Simulando click en: {selected_opt['title']}...")

                active_category = selected_opt["id"]
                
                agent_state["new_answer"] = {
                    "target_field": active_category,
                    "question_text": "",
                    "answer": ""
                }
                
                # 👇 THE FIX: Inject the lock state into the context BEFORE the API call 👇
                if "strategic_context" not in agent_state:
                    agent_state["strategic_context"] = {}
                agent_state["strategic_context"]["active_category"] = active_category
                
                payload_respuesta = {
                    "thread_id": thread_id,
                    "agent_state": agent_state
                }
                
                resp = requests.post(f"{BASE_URL}/process", json=payload_respuesta)
                if resp.status_code != 200:
                    print("❌ Error al enviar la señal:", resp.text)
                    break
                    
                current_job_id = resp.json().get("job_id")
                continue
                
        # =======================================================
        # 🤖 VIEW 2: INTERROGACIÓN (Default o Específica)
        # =======================================================
        preguntas = ia_data.get("questions", [])
        pregunta = preguntas[0] if preguntas else "¿Puedes proporcionar más detalles sobre esto?"
        
        print(f"\n🤖 IA: {pregunta}")
        
        # Normal question flow continues here
        print("\n  [💡 Escribe '/menu' para volver al Dashboard de opciones]")
        respuesta_usuario = input("\n👤 Tu respuesta: ")
        
        if respuesta_usuario.strip().lower() == "/menu":
            has_entered_audit_room = False
            active_category = None
            print("\n🔄 Volviendo al menú principal...")
            continue 
        
        # 👇 THE FIX: Safely lock onto the target field without an else-block intercept 👇
        if active_category:
            cat_name = active_category.split(":")[1]
            gap_actual = next((g["field"] for g in gaps if g.get("ui_category") == cat_name), gaps[0]["field"])
        else:
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