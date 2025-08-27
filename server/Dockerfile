FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar uv para una instalación más rápida de dependencias
RUN pip install uv

# Copiar archivos de requisitos
COPY requirements.txt .
COPY prompt_system.txt .

# Instalar dependencias usando uv
RUN uv pip install --system -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto que utiliza la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]