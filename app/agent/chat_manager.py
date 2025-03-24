from app.agent.deepseek_agent import DeepSeekAgent
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def run_cli_interface(model_name=None):
    """
    CLI 인터페이스 실행
    
    Args:
        model_name: 사용할 모델 이름
    """
    # 에이전트 초기화
    print("🤖 DeepSeek 에이전트 초기화 중...")
    agent = DeepSeekAgent(model_name)
    print("✅ 초기화 완료!")
    
    print("\n🚀 DeepSeek AI 에이전트가 시작되었습니다.")
    print("💡 종료하려면 'exit' 또는 'quit'를 입력하세요.")
    print("💡 대화 기록을 초기화하려면 'clear'를 입력하세요.")
    
    while True:
        user_input = input("\n💬 질문: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("👋 에이전트를 종료합니다.")
            break
        
        if user_input.lower() == "clear":
            print(agent.clear_history())
            continue
        
        print("\n🤔 생각 중...")
        response = agent.generate_response(user_input)
        print(f"\n🤖 응답: {response}")