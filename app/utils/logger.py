import os
import logging
from logging.handlers import RotatingFileHandler
from app.config import Config


def setup_logger(name):
    """
    로거 설정
    
    Args:
        name: 로거 이름
    
    Returns:
        설정된 로거 인스턴스
    """
    logger = logging.getLogger(name)
    
    # 이미 설정된 로거인 경우 반환
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # 포맷 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러
    log_file = os.path.join(Config.LOG_DIR, 'app.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger