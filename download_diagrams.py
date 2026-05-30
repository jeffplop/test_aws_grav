import os
import base64
import urllib.request
import json

diagrams_dir = "Entrega-Final-EP2/evidencias/diagramas"
files = [
    "1-arquitectura-aws.mmd",
    "2-flujo-cicd.mmd",
    "3-comunicacion-red.mmd",
    "4-flujo-despliegue.mmd"
]

def get_mermaid_kroki_url(mermaid_code):
    # Kroki.io is more reliable and free without strict headers
    import zlib
    compressed = zlib.compress(mermaid_code.encode('utf-8'), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    return f"https://kroki.io/mermaid/png/{encoded}"

for filename in files:
    filepath = os.path.join(diagrams_dir, filename)
    outpath = os.path.join(diagrams_dir, filename.replace('.mmd', '.png'))
    
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
        
    url = get_mermaid_kroki_url(code)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(outpath, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Descargado: {outpath}")
    except Exception as e:
        print(f"Error descargando {filename}: {e}")
