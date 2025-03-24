import os
import argparse
from app.config import Config
from app.api.routes import create_app
from app.agent.deepseek_agent import DeepSeekAgent

def parse_arguments():
    """명령줄 인자 파싱"""
    parser = argparse.ArgumentParser(description='DeepSeek AI 에이전트')
    parser.add_argument('--web', action='store_true', help='웹 인터페이스 실행')
    parser.add_argument('--cli', action='store_true', help='CLI 모드 실행')
    parser.add_argument('--port', type=int, default=5000, help='웹 서버 포트')
    parser.add_argument('--model', type=str, default="deepseek-ai/deepseek-coder-6.7b-instruct", 
                        help='사용할 모델 이름')
    return parser.parse_args()

def run_cli(model_name):
    """CLI 모드로 실행"""
    from app.agent.chat_manager import run_cli_interface
    run_cli_interface(model_name)

def run_web(port, model_name):
    """웹 인터페이스 모드로 실행"""
    app = create_app(model_name)
    print(f"🚀 웹 서버가 http://localhost:{port}에서 실행 중입니다")
    
    # Windows에서는 waitress, 그 외에서는 gunicorn 사용
    if os.name == 'nt':  # Windows
        from waitress import serve
        serve(app, host='0.0.0.0', port=port)
    else:  # Linux/Mac
        app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)

def main():
    """메인 진입점"""
    args = parse_arguments()
    
    if args.cli:
        run_cli(args.model)
    else:  # 기본값은 웹 모드
        run_web(args.port, args.model)

if __name__ == "__main__":
    main()