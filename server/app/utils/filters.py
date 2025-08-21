import re

def filter_markdown(text: str ) -> str: 
    markdown_patterns = [
        r'\\[^\\]+\\/',      # Secuencias como \palabra\
        r'```[\s\S]*?```',   # Bloques de código
        r'`[^`]*`',          # Código en línea
        r'^#{1,6}\s*.*$',    # Encabezados
        r'^\s*[-*+]\s+',     # Listas con guiones o asteriscos
        r'^\s*\d+\.\s+',     # Listas numeradas
        r'\[([^\]]*)\]\([^\)]*\)',  # Enlaces
        r'\*\*([^\*]*)\*\*',  # Negrita
        r'__([^_]+)__',      # Negrita
        r'\*([^\*]*)\*',     # Cursiva
        r'_([^_]+)_',        # Cursiva
        r'^\s*>\s+',         # Citas
        r'---+',             # Líneas horizontales
        r'\n\s*\n',          # Líneas vacías múltiples
        r'\\',               # Barras invertidas sueltas
    ]

    combined_pattern = '|'.join(f'({p})' for p in markdown_patterns)

    cleaned_text = re.sub(combined_pattern, '', text, flags=re.MULTILINE)

    cleaned_text = re.sub(r'\s', ' ', cleaned_text)

    return cleaned_text

