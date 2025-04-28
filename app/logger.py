import inspect
import logging
import sys
from datetime import timedelta
from pathlib import Path
from loguru import logger

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
            
        # Find caller from where originated the logged message
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1
            
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )

def setup_logger() -> None:
    # Make sure logs directory exists
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Configure loguru
    logger.remove()  # Remove default handler
    
    # Add file handler
    logger.add(
        logs_dir / "file.log",
        rotation="10 MB",
        retention=timedelta(weeks=1),
        level="INFO",
    )
    
    # Add stdout handler
    logger.add(
        sys.stdout,
        level="INFO",
    )
    
    # Intercept standard library logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # Log a test message
    logger.info("Logger setup complete")