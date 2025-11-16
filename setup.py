"""Setup configuration for Election Prediction MLOps project."""

from setuptools import setup, find_packages

setup(
    name="election-prediction",
    version="1.0.0",
    description="Production MLOps system for election prediction",
    author="MLOps Team",
    author_email="mlops-team@example.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0,<2.0.0",
        "pandas>=2.0.0,<3.0.0",
        "scikit-learn>=1.3.0,<2.0.0",
        "xgboost>=2.0.0,<3.0.0",
        "joblib>=1.3.0,<2.0.0",
        "scipy>=1.11.0,<2.0.0",
        "mlflow>=2.9.0,<3.0.0",
        "evidently>=0.4.0,<1.0.0",
        "fastapi>=0.109.0,<1.0.0",
        "uvicorn[standard]>=0.27.0,<1.0.0",
        "pydantic>=2.5.0,<3.0.0",
        "python-multipart>=0.0.6,<1.0.0",
        "prometheus-client>=0.19.0,<1.0.0",
        "matplotlib>=3.7.0,<4.0.0",
        "seaborn>=0.12.0,<1.0.0",
        "python-dotenv>=1.0.0,<2.0.0",
        "pyyaml>=6.0.0,<7.0.0",
        "requests>=2.31.0,<3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0,<8.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "pytest-asyncio>=0.21.0,<1.0.0",
            "httpx>=0.25.0,<1.0.0",
            "black>=23.7.0,<25.0.0",
            "flake8>=6.0.0,<7.0.0",
            "isort>=5.12.0,<6.0.0",
            "bandit>=1.7.5,<2.0.0",
        ],
        "dvc": [
            "dvc[s3]>=3.0.0,<4.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
