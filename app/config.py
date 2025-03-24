import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """애플리케이션 설정"""
    # 앱 설정
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # 모델 설정
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'deepseek-ai/deepseek-coder-6.7b-instruct')
    DEVICE = os.getenv('DEVICE', 'cuda' if os.getenv('USE_GPU', 'True').lower() in ('true', '1', 't') else 'cpu')
    
    # 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODEL_DIR = os.path.join(DATA_DIR, 'models')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    
    # 오디오 설정
    AUDIO_SAMPLE_RATE = int(os.getenv('AUDIO_SAMPLE_RATE', '22050'))
    
    # API 키 (필요한 경우)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # 학습 설정
    TRAINING_BATCH_SIZE = int(os.getenv('TRAINING_BATCH_SIZE', '4'))
    TRAINING_EPOCHS = int(os.getenv('TRAINING_EPOCHS', '3'))
    LEARNING_RATE = float(os.getenv('LEARNING_RATE', '2e-5'))
    
    # 경로 생성
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)