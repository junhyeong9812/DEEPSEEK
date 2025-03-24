import os
import json
from datasets import Dataset, load_dataset
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class DatasetManager:
    """학습 데이터셋 준비 및 관리 클래스"""
    
    def __init__(self, tokenizer, max_length=512):
        """
        데이터셋 관리자 초기화
        
        Args:
            tokenizer: 사용할 토크나이저
            max_length: 최대 시퀀스 길이
        """
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # 데이터 디렉토리
        self.raw_data_dir = os.path.join(Config.DATA_DIR, "raw")
        self.processed_data_dir = os.path.join(Config.DATA_DIR, "processed")
        
        # 디렉토리 생성
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)
    
    def load_json_data(self, json_file_path):
        """
        JSON 형식의 데이터 로드
        
        Args:
            json_file_path: JSON 파일 경로
            
        Returns:
            데이터셋 객체
        """
        try:
            logger.info(f"JSON 데이터 로드 중: {json_file_path}")
            
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Hugging Face 데이터셋 생성
            dataset = Dataset.from_dict(data)
            logger.info(f"데이터셋 로드 완료: {len(dataset)} 항목")
            
            return dataset
        
        except Exception as e:
            logger.error(f"데이터 로드 중 오류: {str(e)}")
            raise
    
    def load_conversation_data(self, data_path, format_type="chat"):
        """
        대화 데이터 로드
        
        Args:
            data_path: 데이터 경로 (파일 또는 디렉토리)
            format_type: 데이터 형식 ("chat", "instruct" 등)
            
        Returns:
            데이터셋 객체
        """
        try:
            logger.info(f"대화 데이터 로드 중: {data_path}")
            
            if os.path.isfile(data_path) and data_path.endswith('.json'):
                # 단일 JSON 파일
                dataset = self.load_json_data(data_path)
            else:
                # 디렉토리 또는 다른 형식
                dataset = load_dataset(data_path)
                if 'train' in dataset:
                    dataset = dataset['train']
            
            return dataset
        
        except Exception as e:
            logger.error(f"대화 데이터 로드 중 오류: {str(e)}")
            raise
    
    def tokenize_function(self, examples):
        """
        데이터 토큰화 함수
        
        Args:
            examples: 토큰화할 예제
            
        Returns:
            토큰화된 예제
        """
        # 프롬프트 형식에 맞게 텍스트 포맷팅
        texts = []
        for prompt, response in zip(examples["prompt"], examples["response"]):
            formatted_text = f"Human: {prompt}\n\nAssistant: {response}"
            texts.append(formatted_text)
        
        # 토큰화
        tokenized = self.tokenizer(
            texts,
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )
        
        return tokenized
    
    def prepare_dataset(self, dataset):
        """
        학습을 위한 데이터셋 준비
        
        Args:
            dataset: 원본 데이터셋
            
        Returns:
            학습 준비된 데이터셋
        """
        logger.info("학습을 위한 데이터셋 준비 중...")
        
        # 필요한 열이 있는지 확인하고 형식 변환
        required_columns = ["prompt", "response"]
        
        # 열 이름 매핑 (다른 데이터셋 형식 처리)
        if "instruction" in dataset.column_names and "output" in dataset.column_names:
            dataset = dataset.rename_column("instruction", "prompt")
            dataset = dataset.rename_column("output", "response")
        elif "question" in dataset.column_names and "answer" in dataset.column_names:
            dataset = dataset.rename_column("question", "prompt")
            dataset = dataset.rename_column("answer", "response")
        
        # 필수 열이 누락된 경우 오류
        missing_columns = [col for col in required_columns if col not in dataset.column_names]
        if missing_columns:
            raise ValueError(f"데이터셋에 필수 열이 누락되었습니다: {missing_columns}")
        
        # 토큰화
        tokenized_dataset = dataset.map(
            self.tokenize_function,
            batched=True,
            remove_columns=dataset.column_names  # 원본 열 제거
        )
        
        logger.info(f"데이터셋 준비 완료: {len(tokenized_dataset)} 항목")
        return tokenized_dataset