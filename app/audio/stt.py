import os
import tempfile
import whisper
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class SpeechToText:
    """음성을 텍스트로 변환하는 클래스"""
    
    def __init__(self, model_name="base"):
        """
        음성-텍스트 변환기 초기화
        
        Args:
            model_name: Whisper 모델 이름 ('tiny', 'base', 'small', 'medium', 'large')
        """
        try:
            logger.info(f"Whisper 모델 '{model_name}' 로딩 중...")
            self.model = whisper.load_model(model_name)
            logger.info("Whisper 모델 로딩 완료")
        except Exception as e:
            logger.error(f"Whisper 모델 로딩 실패: {str(e)}")
            raise
    
    def transcribe_file(self, audio_file, language=None):
        """
        오디오 파일에서 텍스트 추출
        
        Args:
            audio_file: 오디오 파일 경로
            language: 언어 코드 (예: 'ko', 'en', None=자동감지)
            
        Returns:
            추출된 텍스트
        """
        try:
            logger.info(f"오디오 파일 '{audio_file}' 변환 중...")
            result = self.model.transcribe(
                audio_file,
                language=language,
                fp16=False
            )
            logger.info("오디오 변환 완료")
            return result["text"]
        except Exception as e:
            logger.error(f"오디오 변환 실패: {str(e)}")
            raise
    
    def transcribe_audio_data(self, audio_data, language=None):
        """
        오디오 데이터(바이트)에서 텍스트 추출
        
        Args:
            audio_data: 오디오 데이터 (바이트)
            language: 언어 코드
            
        Returns:
            추출된 텍스트
        """
        try:
            # 임시 파일에 오디오 데이터 저장
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
                temp_file.write(audio_data)
            
            # 변환
            result = self.transcribe_file(temp_filename, language)
            
            # 임시 파일 삭제
            os.unlink(temp_filename)
            
            return result
        except Exception as e:
            logger.error(f"오디오 데이터 변환 실패: {str(e)}")
            raise