import os
import torch
from transformers import Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class DeepSeekTrainer:
    """DeepSeek 모델 학습 및 파인튜닝 클래스"""
    
    def __init__(self, model, tokenizer, dataset):
        """
        학습기 초기화
        
        Args:
            model: 학습할 모델
            tokenizer: 토크나이저
            dataset: 학습 데이터셋
        """
        self.model = model
        self.tokenizer = tokenizer
        self.dataset = dataset
        self.device = Config.DEVICE
        
        # 학습 출력 디렉토리
        self.output_dir = os.path.join(Config.MODEL_DIR, "finetuned_model")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 로깅 디렉토리
        self.logging_dir = os.path.join(Config.LOG_DIR, "training_logs")
        os.makedirs(self.logging_dir, exist_ok=True)
        
        # 데이터 콜레이터 (마스킹된 언어 모델링)
        self.data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False  # 인과적 언어 모델링
        )
    
    def prepare_for_lora_training(self):
        """LoRA 학습을 위한 모델 준비"""
        logger.info("LoRA 파인튜닝을 위한 모델 준비 중...")
        
        # LoRA 설정
        peft_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=8,  # 낮은 랭크
            lora_alpha=32,
            lora_dropout=0.1,
            bias="none",
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
        )
        
        # 원본 모델에 LoRA 적용
        self.model = get_peft_model(self.model, peft_config)
        self.model.print_trainable_parameters()  # 학습 가능한 매개변수 출력
        
        logger.info("LoRA 모델 준비 완료")
        return self.model
    
    def train(self, batch_size=None, epochs=None, learning_rate=None):
        """
        모델 학습 실행
        
        Args:
            batch_size: 배치 크기
            epochs: 에폭 수
            learning_rate: 학습률
            
        Returns:
            학습된 모델
        """
        # 기본값 설정
        batch_size = batch_size or Config.TRAINING_BATCH_SIZE
        epochs = epochs or Config.TRAINING_EPOCHS
        learning_rate = learning_rate or Config.LEARNING_RATE
        
        logger.info(f"학습 시작: 배치 크기={batch_size}, 에폭={epochs}, 학습률={learning_rate}")
        
        # 학습 인자 설정
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            learning_rate=learning_rate,
            weight_decay=0.01,
            logging_dir=self.logging_dir,
            logging_steps=10,
            save_strategy="epoch",
            save_total_limit=2,
            load_best_model_at_end=True,
            fp16=torch.cuda.is_available(),  # 16비트 부동소수점 정밀도 (GPU만)
            gradient_accumulation_steps=4,  # 그래디언트 누적
            warmup_steps=100,  # 웜업 스텝
            report_to=["tensorboard"],
        )
        
        # 학습기 초기화
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=self.data_collator,
            train_dataset=self.dataset,
        )
        
        # 학습 실행
        try:
            trainer.train()
            
            # 모델 저장
            logger.info(f"학습된 모델 저장 중: {self.output_dir}")
            trainer.save_model(self.output_dir)
            self.tokenizer.save_pretrained(self.output_dir)
            
            logger.info("학습 완료!")
            return self.model
            
        except Exception as e:
            logger.error(f"학습 중 오류 발생: {str(e)}")
            raise