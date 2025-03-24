import os
import io
import tempfile
from TTS.api import TTS
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class TextToSpeech:
    """텍스트를 음성으로 변환하는 클래스"""
    
    def __init__(self, model_name=None, language="ko"):
        """
        텍스트-음성 변환기 초기화
        
        Args:
            model_name: TTS 모델 이름 (None=자동 선택)
            language: 언어 코드
        """
        try:
            logger.info("TTS 모델 로딩 중...")
            
            # 모델 이름이 지정되지 않은 경우 언어에 따라 기본 모델 선택
            if model_name is None:
                if language == "ko":
                    model_name = "tts_models/ko/glow-tts/korean-universal"
                else:
                    model_name = "tts_models/en/ljspeech/tacotron2-DDC"
            
            self.tts = TTS(model_name)
            logger.info(f"TTS 모델 '{model_name}' 로딩 완료")
            
            self.language = language
        except Exception as e:
            logger.error(f"TTS 모델 로딩 실패: {str(e)}")
            raise
    
    def synthesize_to_file(self, text, output_file, speaker=None):
        """
        텍스트를 음성 파일로 변환
        
        Args:
            text: 변환할 텍스트
            output_file: 출력 파일 경로
            speaker: 화자 ID (다중 화자 모델인 경우)
            
        Returns:
            출력 파일 경로
        """
        try:
            logger.info(f"텍스트를 음성으로 변환 중...")
            self.tts.tts_to_file(
                text=text,
                file_path=output_file,
                speaker=speaker
            )
            logger.info(f"음성 파일 '{output_file}' 생성 완료")
            return output_file
        except Exception as e:
            logger.error(f"텍스트 음성 변환 실패: {str(e)}")
            raise
    
    def synthesize_to_bytes(self, text, speaker=None):
        """
        텍스트를 음성 바이트로 변환
        
        Args:
            text: 변환할 텍스트
            speaker: 화자 ID (다중 화자 모델인 경우)
            
        Returns:
            음성 데이터 (바이트)
        """
        try:
            # 임시 파일에 음성 저장
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
            
            # 음성 합성
            self.synthesize_to_file(text, temp_filename, speaker)
            
            # 파일 읽기
            with open(temp_filename, 'rb') as f:
                audio_bytes = f.read()
            
            # 임시 파일 삭제
            os.unlink(temp_filename)
            
            return audio_bytes
        except Exception as e:
            logger.error(f"텍스트 음성 변환 실패: {str(e)}")
            raise