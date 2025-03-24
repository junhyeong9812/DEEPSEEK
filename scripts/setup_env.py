import os
import sys
import argparse
import subprocess
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def check_dependencies():
    """필수 의존성 확인"""
    logger.info("필수 의존성 확인 중...")
    
    # 파이썬 버전 확인
    import sys
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        logger.error("파이썬 3.8 이상이 필요합니다.")
        return False
    
    # 필수 패키지 확인
    try:
        import torch
        import transformers
        import flask
        import whisper
        from TTS.api import TTS
        logger.info("모든 필수 패키지가 설치되어 있습니다.")
        return True
    except ImportError as e:
        logger.error(f"필수 패키지가 누락되었습니다: {str(e)}")
        return False

def check_gpu():
    """GPU 사용 가능 여부 확인"""
    logger.info("GPU 확인 중...")
    
    try:
        import torch
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0) if device_count > 0 else "N/A"
            logger.info(f"사용 가능한 GPU: {device_count}개 (첫 번째: {device_name})")
            return True
        else:
            logger.warning("GPU를 사용할 수 없습니다. CPU 모드로 실행됩니다.")
            return False
    except Exception as e:
        logger.error(f"GPU 확인 중 오류: {str(e)}")
        return False

def create_directories():
    """필요한 디렉토리 생성"""
    logger.info("필요한 디렉토리 생성 중...")
    
    directories = [
        "data/raw",
        "data/processed",
        "data/models",
        "data/chat_logs",
        "logs",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"디렉토리 생성됨: {directory}")
    
    # .gitkeep 파일 생성
    for directory in ["data/raw", "data/processed", "data/models"]:
        gitkeep_file = os.path.join(directory, ".gitkeep")
        if not os.path.exists(gitkeep_file):
            with open(gitkeep_file, 'w') as f:
                pass
    
    return True

def install_dependencies(force=False):
    """의존성 설치"""
    logger.info("의존성 설치 중...")
    
    if not force and check_dependencies():
        logger.info("이미 모든 의존성이 설치되어 있습니다.")
        return True
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("의존성 설치 완료")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"의존성 설치 실패: {str(e)}")
        return False

def create_env_file():
    """환경 변수 파일 생성"""
    logger.info(".env 파일 생성 중...")
    
    env_file = ".env"
    if os.path.exists(env_file):
        logger.info(".env 파일이 이미 존재합니다.")
        return True
    
    try:
        with open(env_file, 'w') as f:
            f.write("""# 애플리케이션 설정
DEBUG=True
SECRET_KEY=your-secret-key-change-me

# 모델 설정
DEFAULT_MODEL=deepseek-ai/deepseek-coder-6.7b-instruct
USE_GPU=True

# API 키
OPENAI_API_KEY=YOUR-API-KEY

# 학습 설정
TRAINING_BATCH_SIZE=4
TRAINING_EPOCHS=3
LEARNING_RATE=2e-5
""")
        logger.info(".env 파일 생성 완료")
        return True
    except Exception as e:
        logger.error(f".env 파일 생성 실패: {str(e)}")
        return False

def main():
    """스크립트 진입점"""
    parser = argparse.ArgumentParser(description="환경 설정 스크립트")
    parser.add_argument("--force", action="store_true", help="의존성 강제 재설치")
    parser.add_argument("--skip-deps", action="store_true", help="의존성 설치 건너뛰기")
    
    args = parser.parse_args()
    
    # 디렉토리 생성
    create_directories()
    
    # GPU 확인
    check_gpu()
    
    # 의존성 설치
    if not args.skip_deps:
        install_dependencies(args.force)
    
    # 환경 변수 파일 생성
    create_env_file()
    
    logger.info("환경 설정이 완료되었습니다.")

if __name__ == "__main__":
    import sys
    main()