from setuptools import setup, find_packages

setup(
    name="ai-dna-charter",
    version="2.1.1",
    author="TerisC",
    description="AI-DNA Charter Framework for Ethical AI Systems",
    long_description=open("../README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Teris/AI-DNA-Charta",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8"],
        "docker": ["docker>=5.0.0"],
    },
    entry_points={
        "console_scripts": [
            "ai-dna-demo=ai_dna_framework:demo_chartered_ai",
        ],
    },
)
