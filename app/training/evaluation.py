import numpy as np
import torch
from tqdm import tqdm
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class ModelEvaluator:
    """모델 평가 및 성능 측정 클래스"""
    
    def __init__(self, model, tokenizer):
        """
        평가기 초기화
        
        Args:
            model: 평가할 모델
            tokenizer: 토크나이저
        """
        self.model = model
        self.tokenizer = tokenizer
        self.device = Config.DEVICE
    
    def evaluate_perplexity(self, eval_dataset):
        """
        데이터셋에 대한 퍼플렉시티 계산
        
        Args:
            eval_dataset: 평가 데이터셋
            
        Returns:
            퍼플렉시티 (낮을수록 좋음)
        """
        logger.info("모델 퍼플렉시티 평가 중...")
        
        self.model.eval()
        total_loss = 0
        total_tokens = 0
        
        with torch.no_grad():
            for batch in tqdm(eval_dataset, desc="평가 중"):
                # 배치를 장치로 이동
                inputs = {k: v.to(self.device) for k, v in batch.items()}
                
                # 정방향 패스
                outputs = self.model(**inputs, labels=inputs["input_ids"])
                loss = outputs.loss.item()
                
                # 패딩 토큰을 제외한 토큰 수 계산
                non_pad_mask = inputs["input_ids"] != self.tokenizer.pad_token_id
                num_tokens = non_pad_mask.sum().item()
                
                total_loss += loss * num_tokens
                total_tokens += num_tokens
        
        # 퍼플렉시티 계산 (평균 손실의 지수)
        avg_loss = total_loss / total_tokens
        perplexity = np.exp(avg_loss)
        
        logger.info(f"평가 완료: 퍼플렉시티 = {perplexity:.4f}")
        return perplexity
    
    def evaluate_samples(self, test_prompts, max_length=100, temperature=0.7):
        """
        샘플 프롬프트에 대한 모델 응답 생성 및 평가
        
        Args:
            test_prompts: 테스트 프롬프트 목록
            max_length: 최대 생성 길이
            temperature: 샘플링 온도
            
        Returns:
            응답 목록
        """
        logger.info(f"{len(test_prompts)}개 샘플 프롬프트에 대한 모델 평가 중...")
        
        self.model.eval()
        responses = []
        
        for prompt in tqdm(test_prompts, desc="샘플 평가 중"):
            try:
                # DeepSeek 형식으로 프롬프트 포맷팅
                formatted_prompt = f"Human: {prompt}\n\nAssistant:"
                
                # 입력 토큰화
                inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.device)
                
                # 응답 생성
                with torch.no_grad():
                    generated_ids = self.model.generate(
                        inputs.input_ids,
                        max_length=max_length,
                        temperature=temperature,
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id
                    )
                
                # 생성된 텍스트 디코딩
                response_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
                
                # 프롬프트 부분 제거하고 응답만 추출
                response = response_text[len(formatted_prompt):].strip()
                responses.append(response)
                
            except Exception as e:
                logger.error(f"샘플 '{prompt}' 평가 중 오류: {str(e)}")
                responses.append(f"오류: {str(e)}")
        
        logger.info("샘플 평가 완료")
        return responses