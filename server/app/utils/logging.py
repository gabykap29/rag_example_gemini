import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.config.config import log_directory, log_level, log_to_file

# Crear directorio de logs si no existe
log_dir = Path(log_directory)
log_dir.mkdir(exist_ok=True)

# Configuración básica del logger
def setup_logger(name, custom_log_level=None):
    """
    Configura y devuelve un logger con el nombre especificado.
    
    Args:
        name: Nombre del logger (normalmente __name__ del módulo)
        custom_log_level: Nivel de logging específico (si es None, se usa el nivel del entorno)
        
    Returns:
        Logger configurado
    """
    # Determinar el nivel de logging basado en el entorno o el parámetro
    if custom_log_level is None:
        # Usar el nivel de log configurado en config.py
        configured_level = log_level.upper()
        log_level_value = getattr(logging, configured_level, logging.INFO)
    else:
        log_level_value = custom_log_level
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level_value)
    
    # Evitar duplicación de handlers
    if not logger.handlers:
        # Formato del log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(thread)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler para archivo con rotación (solo si está habilitado)
        if log_to_file:
            file_handler = RotatingFileHandler(
                log_dir / f"{name.split('.')[-1]}.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger

# Logger para acceso a la API
api_logger = setup_logger('app.api')

# Logger para servicios
service_logger = setup_logger('app.services')

# Logger para core
core_logger = setup_logger('app.core')

# Logger para errores generales
error_logger = setup_logger('app.errors', logging.ERROR)