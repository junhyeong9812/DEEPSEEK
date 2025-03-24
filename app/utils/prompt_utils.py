class PromptTemplates:
    """다양한 작업을 위한 프롬프트 템플릿"""
    
    @staticmethod
    def code_optimization(code):
        """
        코드 최적화 프롬프트
        
        Args:
            code: 최적화할 코드
            
        Returns:
            포맷팅된 프롬프트
        """
        return f"""다음 코드를 최적화해 주세요. 성능과 가독성을 개선하세요.

```python
{code}
```

최적화된 코드와 함께 변경 사항에 대한 설명을 제공해 주세요."""
    
    @staticmethod
    def code_refactoring(code):
        """
        코드 리팩토링 프롬프트
        
        Args:
            code: 리팩토링할 코드
            
        Returns:
            포맷팅된 프롬프트
        """
        return f"""다음 코드를 리팩토링해 주세요. 클린 코드 원칙을 적용하세요.

```python
{code}
```

리팩토링된 코드와 함께 적용한 리팩토링 패턴 및 개선 사항을 설명해 주세요."""
    
    @staticmethod
    def code_explanation(code):
        """
        코드 설명 프롬프트
        
        Args:
            code: 설명할 코드
            
        Returns:
            포맷팅된 프롬프트
        """
        return f"""다음 코드를 상세히 설명해 주세요. 각 부분의 역할과 로직을 설명하세요.

```python
{code}
```

코드의 주요 기능, 알고리즘, 중요한 부분에 초점을 맞추어 설명해 주세요."""
    
    @staticmethod
    def bug_fixing(code, error_message=None):
        """
        버그 수정 프롬프트
        
        Args:
            code: 수정할 코드
            error_message: 오류 메시지 (옵션)
            
        Returns:
            포맷팅된 프롬프트
        """
        prompt = f"""다음 코드에서 버그를 찾아 수정해 주세요.

```python
{code}
```"""

        if error_message:
            prompt += f"""

발생한 오류 메시지:
```
{error_message}
```"""

        prompt += """

수정된 코드와 함께 문제가 무엇이었는지, 어떻게 수정했는지 설명해 주세요."""
        return prompt
    
    @staticmethod
    def code_completion(code):
        """
        코드 완성 프롬프트
        
        Args:
            code: 완성할 코드 일부
            
        Returns:
            포맷팅된 프롬프트
        """
        return f"""다음 코드를 완성해 주세요.

```python
{code}
```

코드의 의도를 파악하여 나머지 부분을 작성해 주세요. 필요한 기능을 추가하고 누락된 부분을 채워 넣으세요."""
    
    @staticmethod
    def learning_instruction(topic):
        """
        학습 지침 프롬프트
        
        Args:
            topic: 학습 주제
            
        Returns:
            포맷팅된 프롬프트
        """
        return f"""'{topic}'에 대한 학습 자료를 생성해 주세요.

다음 구성으로 작성해 주세요:
1. 주제 소개
2. 핵심 개념
3. 간단한 예제
4. 실습 과제
5. 심화 학습 방향

초보자도 이해할 수 있도록 명확하고 단계적으로 설명해 주세요."""