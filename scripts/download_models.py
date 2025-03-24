import os
import sys
import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM
import whisper
from TTS.api import TTS

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.config import Config
from app.utils.logger import setup_logger


logger = setup_logger(__name__)

def download_deepseek_model(model_name=None):
    """DeepSeek 모델 다운로드"""
    model_name = model_name or Config.DEFAULT_MODEL
    logger.info(f"DeepSeek 모델 '{model_name}' 다운로드 중...")
    
    try:
        # 토크나이저 다운로드
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(os.path.join(Config.MODEL_DIR, "deepseek_tokenizer"))
        
        # 모델 다운로드
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            trust_remote_code=True
        )
        model.save_pretrained(os.path.join(Config.MODEL_DIR, "deepseek_model"))
        
        logger.info(f"DeepSeek 모델 다운로드 완료")
        return True
    except Exception as e:
        logger.error(f"DeepSeek 모델 다운로드 실패: {str(e)}")
        return False

def download_whisper_model(model_name="base"):
    """Whisper 모델 다운로드"""
    logger.info(f"Whisper 모델 '{model_name}' 다운로드 중...")
    
    try:
        whisper.load_model(model_name)
        logger.info(f"Whisper 모델 다운로드 완료")
        return True
    except Exception as e:
        logger.error(f"Whisper 모델 다운로드 실패: {str(e)}")
        return False

def download_tts_model(model_name=None):
    """TTS 모델 다운로드"""
    try:
        if model_name is None:
            # 다국어 지원 모델 사용
            model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

        logger.info(f"TTS 모델 '{model_name}' 다운로드 중...")

        # GPU 사용 비활성화하여 호환성 문제 해결
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        
        # TTS 모델 로드
        from TTS.api import TTS
        tts = TTS(model_name=model_name, progress_bar=False)
        
        # 간단한 텍스트로 테스트 (선택 사항)
        test_text = "안녕하세요. 테스트입니다."
        logger.info(f"TTS 모델 테스트: '{test_text}'")
        
        logger.info("TTS 모델 다운로드 완료")
        return True

    except Exception as e:
        logger.error(f"TTS 모델 다운로드 실패: {str(e)}")
        
        # 실패 시 대체 모델 시도
        try:
            logger.info("대체 다국어 모델 시도 중...")
            alt_model = "tts_models/multilingual/multi-dataset/your_tts"
            
            # GPU 사용 비활성화
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
            
            from TTS.api import TTS
            tts = TTS(model_name=alt_model, progress_bar=False)
            
            logger.info("대체 TTS 모델 다운로드 완료")
            return True
        except Exception as e2:
            logger.error(f"대체 TTS 모델 다운로드도 실패: {str(e2)}")
            return False



def main():
    """스크립트 진입점"""
    parser = argparse.ArgumentParser(description="모델 다운로드 스크립트")
    parser.add_argument("--all", action="store_true", help="모든 모델 다운로드")
    parser.add_argument("--deepseek", action="store_true", help="DeepSeek 모델 다운로드")
    parser.add_argument("--whisper", action="store_true", help="Whisper 모델 다운로드")
    parser.add_argument("--tts", action="store_true", help="TTS 모델 다운로드")
    parser.add_argument("--deepseek-model", type=str, default=None, help="다운로드할 DeepSeek 모델 이름")
    parser.add_argument("--whisper-model", type=str, default="base", help="다운로드할 Whisper 모델 이름")
    parser.add_argument("--language", type=str, default="ko", help="TTS 모델 언어")
    
    args = parser.parse_args()
    
    # 기본값: 플래그가 지정되지 않으면 모두 다운로드
    download_all = args.all or not (args.deepseek or args.whisper or args.tts)
    
    success = True
    
    # DeepSeek 모델 다운로드
    if download_all or args.deepseek:
        if not download_deepseek_model(args.deepseek_model):
            success = False
    
    # Whisper 모델 다운로드
    if download_all or args.whisper:
        if not download_whisper_model(args.whisper_model):
            success = False
    
    
    # TTS 모델 다운로드
    if download_all or args.tts:
        if not download_tts_model():
            success = False
    
    if success:
        logger.info("모든 모델이 성공적으로 다운로드되었습니다.")
    else:
        logger.warning("일부 모델 다운로드가 실패했습니다. 로그를 확인하세요.")

if __name__ == "__main__":
    main()