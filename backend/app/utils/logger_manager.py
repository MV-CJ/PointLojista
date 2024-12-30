import logging
import colorlog
import uuid

# Configuração do logger
logger = logging.getLogger("LoggerManage")
logger.setLevel(logging.DEBUG)

# Configuração do manipulador de console com cores
console_handler = colorlog.StreamHandler()
console_handler.setLevel(logging.DEBUG)


# Formatação com cores e incluindo a rota
formatter = colorlog.ColoredFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(log_color)s%(message)s',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

