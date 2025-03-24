from flask import Flask, request, jsonify, render_template
from app.agent.deepseek_agent import DeepSeekAgent
from app.config import Config
from app.api.handlers import chat_handler, enhance_code_handler
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def create_app(model_name=None):
    """Flask 앱 생성 및 설정"""
    app = Flask(__name__, 
                template_folder=Config.BASE_DIR + '/templates',
                static_folder=Config.BASE_DIR + '/static')
    
    # 앱 설정
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['DEBUG'] = Config.DEBUG
    
    # 에이전트 인스턴스
    agent = DeepSeekAgent(model_name)
    
    @app.route('/')
    def home():
        """홈페이지"""
        return render_template('index.html')
    
    @app.route('/chat')
    def chat_page():
        """채팅 페이지"""
        return render_template('chat.html')
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """채팅 API 엔드포인트"""
        data = request.json
        return chat_handler(agent, data)
    
    @app.route('/api/enhance', methods=['POST'])
    def enhance():
        """코드 향상 API 엔드포인트"""
        data = request.json
        return enhance_code_handler(agent, data)
    
    @app.errorhandler(404)
    def page_not_found(e):
        """404 오류 핸들러"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        """500 오류 핸들러"""
        logger.error(f"서버 오류: {str(e)}")
        return jsonify({"error": "내부 서버 오류가 발생했습니다."}), 500
    
    return app