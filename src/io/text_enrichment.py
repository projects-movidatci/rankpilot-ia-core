import re
from docxtpl import RichText

def parse_markdown_to_richtext(text_string: str) -> RichText:
    """
    Converts bold (**text**) and colored (<red>text</red>) markdown to RichText.
    Forces line breaks and parses markdown bullets.
    """
    if not text_string or not isinstance(text_string, str):
        return text_string 

    rt = RichText()
    text_string = text_string.replace('\r\n', '\n')
    
    # 🛡️ THE FIX: Failsafe for inline bullets. 
    # If the LLM generates "...markets. * Cross-Border" without a newline, 
    # this forces a newline before the asterisk so the parser catches it.
    text_string = re.sub(r'(?<=\S)\s+\*\s+', '\n* ', text_string)
    
    # Standardize paragraph spacing
    text_string = text_string.replace('\n\n', '\n\n\n')
    lineas = text_string.split('\n')

    # 🛡️ THE FIX: Process everything in a SINGLE loop to prevent variable scope loss.
    for index, linea in enumerate(lineas):
        
        # 1. Detect and transform bullets BEFORE processing bold/color
        if re.match(r'^\s*[-*]\s+', linea):
            # Replace the markdown bullet with a real bullet and a tab for clean spacing
            linea = re.sub(r'^\s*[-*]\s+', '•\t', linea)

        if linea == "":
            if index < len(lineas) - 1:
                rt.add('\n')
            continue
            
        # 2. First split by <red> tags
        tokens_rojos = re.split(r'\[RED_START\](.*?)\[RED_END\]', linea)
        
        for i, token in enumerate(tokens_rojos):
            if not token:
                continue
            
            es_rojo = (i % 2 != 0) # Inside <red> falls on odd indices
            
            # 3. Then split by bold tags
            partes_negritas = re.split(r'\*\*(.*?)\*\*', token)
            
            for j, parte in enumerate(partes_negritas):
                if not parte:
                    continue
                
                es_negrita = (j % 2 != 0)
                
                # 4. Apply combined Word styles
                if es_rojo and es_negrita:
                    rt.add(parte, bold=True, color='FF0000') # Pure Red
                elif es_rojo:
                    rt.add(parte, color='FF0000')
                elif es_negrita:
                    rt.add(parte, bold=True)
                else:
                    rt.add(parte)
        
        # Add line break at the end of the paragraph
        if index < len(lineas) - 1:
            rt.add('\n')
            
    return rt

def convert_all_markdown_to_richtext(data):
    """
    Recursively scans a dictionary or list and converts any **bold** strings, 
    bullet points (* or -), OR strings with linebreaks (\n) into docxtpl RichText objects.
    """
    if isinstance(data, dict):
        for k, v in data.items():
            # 🛡️ THE FIX: Broadened the trigger condition to catch strings that only contain an asterisk
            if isinstance(v, str) and ('**' in v or '\n' in v or '*' in v):
                data[k] = parse_markdown_to_richtext(v)
            elif isinstance(v, (dict, list)):
                convert_all_markdown_to_richtext(v)
                
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], str) and ('**' in data[i] or '\n' in data[i] or '*' in data[i]):
                data[i] = parse_markdown_to_richtext(data[i])
            elif isinstance(data[i], (dict, list)):
                convert_all_markdown_to_richtext(data[i])