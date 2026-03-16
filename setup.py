from setuptools import setup, find_packages

setup(
    name="terminalmind",
    version="1.0.0",
    description="AI-Powered System Assistant for Windows",
    author="Shomya Soneji",
    packages=find_packages(),
    install_requires=[
        "langchain==1.2.10",
        "langchain-core==1.2.18",
        "langchain-groq==1.1.2",
        "python-dotenv==1.1.1",
        "rich==13.7.1",
        "joblib==1.5.1",
        "numpy==1.26.4",
        "pandas==2.2.2",
        "scikit-learn==1.2.2",
    ],
    entry_points={
        'console_scripts': [
            'terminalmind=terminalmind.main:main',
        ],
    },
    python_requires='>=3.8',
)