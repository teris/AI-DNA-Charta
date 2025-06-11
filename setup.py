from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="ai-dna-charter",
    version="2.1.1",
    author="TerisC",
    author_email="",
    description="AI-DNA Charter System - Ethical AI Framework with Multilingual Support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teris/AI-DNA-Charter",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'framework': ['languages/*.xml'],
        'schemas': ['*.yaml'],
        'examples': ['**/*.yaml', '**/*.json'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
        "requests>=2.25.0",
        "pyyaml>=6.0",
        "psutil>=5.8.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'black',
            'flake8',
        ],
        'deepseek': [
            'numpy>=1.24.0',
            'transformers>=4.30.0',
            'torch>=2.0.0',
        ],
        'docs': [
            'sphinx>=4.0',
            'sphinx-rtd-theme',
        ],
    },
    entry_points={
        'console_scripts': [
            'ai-dna-charter=tools.charter_cli:main',
            'ai-dna-system=tools.system_manager:main',
            'ai-dna-demo=framework.ai_dna_framework:demo_chartered_ai_extended',
        ],
    },
)
