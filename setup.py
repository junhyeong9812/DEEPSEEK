from setuptools import setup, find_packages

setup(
    name="deepseek-agent",
    version="0.1.0",
    description="DeepSeek 기반 AI 에이전트",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "flask>=2.2.5",
        "transformers>=4.35.0",
        "torch>=2.1.0",
        "openai-whisper>=20230918",
        "TTS>=0.22.0",
        "peft>=0.5.0",
        "datasets>=2.14.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "deepseek-agent=app.main:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)