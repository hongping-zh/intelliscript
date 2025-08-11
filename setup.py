#!/usr/bin/env python3
"""
Enhanced setup script for IntelliScript CLI
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "IntelliScript CLI: Advanced AI Model Management & Cost Optimization"

# Read requirements safely
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    try:
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return ['click>=8.0.0', 'requests>=2.25.0']

setup(
    name="intelliscript-cli",
    version="1.0.0",
    description="Enterprise AI Model Management Platform with Cost Optimization",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="IntelliScript Team",
    author_email="hongping-zh@intelliscript.dev",
    url="https://github.com/hongping-zh/intelliscript",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'intelliscript=intelliscript_cli:cli',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai, cli, model-management, cost-optimization, enterprise",
    python_requires=">=3.8",
    license="MIT",
    project_urls={
        "Bug Reports": "https://github.com/hongping-zh/intelliscript/issues",
        "Source": "https://github.com/hongping-zh/intelliscript",
        "Documentation": "https://github.com/hongping-zh/intelliscript/wiki",
    },
)
