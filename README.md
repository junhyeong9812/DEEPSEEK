# DeepSeek AI 에이전트

DeepSeek Coder 모델 기반의 AI 에이전트로, 코드 개발 지원, 음성 처리, 대화형 인터페이스를 제공합니다.

## 기능

- **코드 개발 지원**: 코드 작성, 최적화, 리팩토링, 버그 수정
- **오디오 처리**: STT(음성-텍스트)와 TTS(텍스트-음성) 변환
- **대화형 인터페이스**: 맥락을 이해하는 자연스러운 대화
- **모델 학습**: LoRA를 이용한 효율적인 파인튜닝

## 설치

```bash
# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

## 사용법

### CLI 모드

```bash
python -m app.main --cli
```

### 웹 인터페이스 모드

```bash
python -m app.main --web --port 5000
```

웹 브라우저에서 http://localhost:5000 을 열어 사용하세요.

## 환경 설정

`.env` 파일을 루트 디렉토리에 생성하고 다음과 같이 설정하세요:

```ini
# 애플리케이션 설정
DEBUG=True
SECRET_KEY=your-secret-key-change-me

# 모델 설정
DEFAULT_MODEL=deepseek-ai/deepseek-coder-6.7b-instruct
USE_GPU=True

# API 키
OPENAI_API_KEY=your-openai-api-key

# 학습 설정
TRAINING_BATCH_SIZE=4
TRAINING_EPOCHS=3
LEARNING_RATE=2e-5
```

## 시스템 요구사항

- **Python**: 3.8 이상
- **GPU**: DeepSeek 모델을 효율적으로 실행하려면 최소 16GB VRAM 권장
- **저장공간**: 모델 다운로드를 위해 최소 20GB 필요

## 학습 방법

커스텀 데이터로 모델을 파인튜닝하려면:

1. `data/raw` 디렉토리에 학습 데이터를 준비합니다.
2. 다음 명령어를 실행합니다:

```bash
python -m app.training.run_training --data_path data/raw/your_data.json
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
