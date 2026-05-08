import re
from docxtpl import RichText

def parse_markdown_to_richtext(text_string: str) -> RichText:
    """
    Convierte negritas (**texto**) y colores (<red>texto</red>) a RichText.
    Fuerza saltos de línea exagerados para Word.
    """
    if not text_string or not isinstance(text_string, str):
        return text_string 

    rt = RichText()
    text_string = text_string.replace('\n\n', '\n\n\n')
    lineas = text_string.split('\n')
    
    for index, linea in enumerate(lineas):
        if linea == "":
            if index < len(lineas) - 1:
                rt.add('\n')
            continue
            
        # 1. Primero cortamos por la etiqueta <red>
        tokens_rojos = re.split(r'\[RED_START\](.*?)\[RED_END\]', linea)
        
        for i, token in enumerate(tokens_rojos):
            if not token:
                continue
            
            es_rojo = (i % 2 != 0) # Lo que está dentro de <red> cae en índices impares
            
            # 2. Luego cortamos por negritas dentro de cada token
            partes_negritas = re.split(r'\*\*(.*?)\*\*', token)
            
            for j, parte in enumerate(partes_negritas):
                if not parte:
                    continue
                
                es_negrita = (j % 2 != 0)
                
                # 3. Aplicamos los estilos combinados a Word
                if es_rojo and es_negrita:
                    rt.add(parte, bold=True, color='FF0000') # FF0000 es Rojo puro
                elif es_rojo:
                    rt.add(parte, color='FF0000')
                elif es_negrita:
                    rt.add(parte, bold=True)
                else:
                    rt.add(parte)
        
        # Salto de línea al final del párrafo
        if index < len(lineas) - 1:
            rt.add('\n')
            
    return rt

def convert_all_markdown_to_richtext(data):
    """
    Recursively scans a dictionary or list and converts any **bold** strings 
    OR strings with linebreaks (\n) into docxtpl RichText objects in place.
    """

    if isinstance(data, dict):
        for k, v in data.items():
            # AHORA ATRAPA TEXTOS CON ASTERISCOS O CON SALTOS DE LÍNEA
            if isinstance(v, str) and ('**' in v or '\n' in v):
                data[k] = parse_markdown_to_richtext(v)
            elif isinstance(v, (dict, list)):
                convert_all_markdown_to_richtext(v)
                
    elif isinstance(data, list):
        for i in range(len(data)):
            # AHORA ATRAPA TEXTOS CON ASTERISCOS O CON SALTOS DE LÍNEA
            if isinstance(data[i], str) and ('**' in data[i] or '\n' in data[i]):
                data[i] = parse_markdown_to_richtext(data[i])
            elif isinstance(data[i], (dict, list)):
                convert_all_markdown_to_richtext(data[i])