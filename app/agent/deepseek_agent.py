import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class DeepSeekAgent:
    """DeepSeek 모델 기반 AI 에이전트"""
    
    def __init__(self, model_name=None):
        """
        DeepSeek 모델 기반 에이전트 초기화
        
        Args:
            model_name: 사용할 모델 이름 (기본값: Config.DEFAULT_MODEL)
        """
        self.model_name = model_name or Config.DEFAULT_MODEL
        self.device = Config.DEVICE
        
        if self.device == "cuda" and not torch.cuda.is_available():
            logger.warning("CUDA를 사용할 수 없습니다. CPU로 전환합니다.")
            self.device = "cpu"
        
        logger.info(f"장치: {self.device}, 모델: {self.model_name}")
        
        # 토크나이저와 모델 로드
        self._load_model()
        
        # 대화 기록 저장
        self.conversation_history = []
    
    def _load_model(self):
        """토크나이저와 모델 로드"""
        logger.info("모델 로딩 중...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                trust_remote_code=True
            ).to(self.device)
            logger.info("모델 로딩 완료!")
        except Exception as e:
            logger.error(f"모델 로딩 실패: {str(e)}")
            raise
    
    def add_to_history(self, role, content):
        """대화 기록에 새 메시지 추가"""
        self.conversation_history.append({"role": role, "content": content})
    
    def format_prompt(self, query):
        """DeepSeek 형식에 맞게 프롬프트 포맷팅"""
        formatted_prompt = ""
        for message in self.conversation_history:
            if message["role"] == "user":
                formatted_prompt += f"Human: {message['content']}\n\n"
            else:
                formatted_prompt += f"Assistant: {message['content']}\n\n"
        
        # 새 쿼리 추가
        formatted_prompt += f"Human: {query}\n\nAssistant:"
        return formatted_prompt
    
    def generate_response(self, query, max_length=2048, temperature=0.7):
        """
        사용자 질문에 응답 생성
        
        Args:
            query: 사용자 질문
            max_length: 최대 토큰 생성 길이
            temperature: 응답 다양성 (낮을수록 결정적)
        
        Returns:
            생성된 텍스트 응답
        """
        # 사용자 쿼리를 기록에 추가
        self.add_to_history("user", query)
        
        # 프롬프트 포맷팅
        prompt = self.format_prompt(query)
        
        # 입력 토큰화
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        try:
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
            response = response_text[len(prompt):].strip()
            
            # 응답을 기록에 추가
            self.add_to_history("assistant", response)
            
            return response
        
        except Exception as e:
            logger.error(f"응답 생성 중 오류 발생: {str(e)}")
            error_msg = f"오류가 발생했습니다: {str(e)}"
            self.add_to_history("assistant", error_msg)
            return error_msg
    
    def clear_history(self):
        """대화 기록 초기화"""
        self.conversation_history = []
        return "대화 기록이 초기화되었습니다."