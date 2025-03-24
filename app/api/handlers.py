from flask import jsonify
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def chat_handler(agent, data):
    """
    채팅 요청 처리
    
    Args:
        agent: DeepSeekAgent 인스턴스
        data: 요청 데이터
    
    Returns:
        Flask 응답
    """
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "질문이 없습니다."}), 400
    
    if query.lower() == 'clear':
        return jsonify({"response": agent.clear_history()})
    
    try:
        # 선택적 매개변수
        max_length = data.get('max_length', 2048)
        temperature = data.get('temperature', 0.7)
        
        response = agent.generate_response(query, max_length, temperature)
        return jsonify({"response": response})
    
    except Exception as e:
        logger.error(f"채팅 처리 중 오류: {str(e)}")
        return jsonify({"error": f"요청 처리 중 오류가 발생했습니다: {str(e)}"}), 500

def enhance_code_handler(agent, data):
    """
    코드 향상 요청 처리
    
    Args:
        agent: DeepSeekAgent 인스턴스
        data: 요청 데이터
    
    Returns:
        Flask 응답
    """
    code = data.get('code', '')
    task = data.get('task', 'optimize')
    
    if not code:
        return jsonify({"error": "코드가 없습니다."}), 400
    
    tasks = {
        "optimize": "다음 코드를 최적화해 주세요. 성능과 가독성을 개선하세요.",
        "refactor": "다음 코드를 리팩토링해 주세요. 클린 코드 원칙을 적용하세요.",
        "explain": "다음 코드를 상세히 설명해 주세요. 각 부분의 역할과 로직을 설명하세요."
    }
    
    prompt = f"{tasks.get(task, tasks['optimize'])}\n\n```python\n{code}\n```"
    
    try:
        response = agent.generate_response(prompt)
        return jsonify({"response": response})
    
    except Exception as e:
        logger.error(f"코드 향상 중 오류: {str(e)}")
        return jsonify({"error": f"요청 처리 중 오류가 발생했습니다: {str(e)}"}), 500