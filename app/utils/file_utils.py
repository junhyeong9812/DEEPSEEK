import os
import json
import yaml
import pickle
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def ensure_dir(directory):
    """
    디렉토리가 존재하는지 확인하고 없으면 생성
    
    Args:
        directory: 확인할 디렉토리 경로
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"디렉토리 생성됨: {directory}")

def save_json(data, filepath, indent=2):
    """
    데이터를 JSON 파일로 저장
    
    Args:
        data: 저장할 데이터
        filepath: 저장 경로
        indent: JSON 들여쓰기 (기본값: 2)
    """
    try:
        # 디렉토리 확인
        ensure_dir(os.path.dirname(filepath))
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        
        logger.info(f"JSON 파일 저장됨: {filepath}")
    except Exception as e:
        logger.error(f"JSON 파일 저장 중 오류: {str(e)}")
        raise

def load_json(filepath):
    """
    JSON 파일에서 데이터 로드
    
    Args:
        filepath: 로드할 파일 경로
        
    Returns:
        로드된 데이터
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"JSON 파일 로드됨: {filepath}")
        return data
    except Exception as e:
        logger.error(f"JSON 파일 로드 중 오류: {str(e)}")
        raise

def save_yaml(data, filepath):
    """
    데이터를 YAML 파일로 저장
    
    Args:
        data: 저장할 데이터
        filepath: 저장 경로
    """
    try:
        # 디렉토리 확인
        ensure_dir(os.path.dirname(filepath))
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        
        logger.info(f"YAML 파일 저장됨: {filepath}")
    except Exception as e:
        logger.error(f"YAML 파일 저장 중 오류: {str(e)}")
        raise

def load_yaml(filepath):
    """
    YAML 파일에서 데이터 로드
    
    Args:
        filepath: 로드할 파일 경로
        
    Returns:
        로드된 데이터
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        logger.info(f"YAML 파일 로드됨: {filepath}")
        return data
    except Exception as e:
        logger.error(f"YAML 파일 로드 중 오류: {str(e)}")
        raise

def save_pickle(data, filepath):
    """
    데이터를 피클 파일로 저장
    
    Args:
        data: 저장할 데이터
        filepath: 저장 경로
    """
    try:
        # 디렉토리 확인
        ensure_dir(os.path.dirname(filepath))
        
        # 파일 저장
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"피클 파일 저장됨: {filepath}")
    except Exception as e:
        logger.error(f"피클 파일 저장 중 오류: {str(e)}")
        raise

def load_pickle(filepath):
    """
    피클 파일에서 데이터 로드
    
    Args:
        filepath: 로드할 파일 경로
        
    Returns:
        로드된 데이터
    """
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        logger.info(f"피클 파일 로드됨: {filepath}")
        return data
    except Exception as e:
        logger.error(f"피클 파일 로드 중 오류: {str(e)}")
        raise

def list_files(directory, extension=None):
    """
    디렉토리 내 파일 목록 반환
    
    Args:
        directory: 검색할 디렉토리
        extension: 파일 확장자 필터 (예: '.py', '.json')
        
    Returns:
        파일 경로 목록
    """
    files = []
    
    try:
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if extension is None or filename.endswith(extension):
                    files.append(os.path.join(root, filename))
        
        return files
    except Exception as e:
        logger.error(f"파일 목록 조회 중 오류: {str(e)}")
        raise