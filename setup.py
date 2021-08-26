from pathlib import Path

from setuptools import setup


BASE_DIR = Path(__file__).parent


with open(BASE_DIR / "requirements.txt") as file:
    required_packages = [ln.strip() for ln in file.readlines()]


dev_packages = [
    "black",
    "flake8",
    "isort",
    "mypy",
    "pytest",
]


setup(
    name="clip-image-search",
    version="0.1",
    license="MIT",
    description="Use OpenAI's CLIP model to search images with text or image as query.",
    author="King Yiu Suen",
    author_email="kingyiusuen@gmail.com",
    url="https://github.com/kingyiusuen/clip-image-search/",
    keywords=[
        "machine-learning",
        "deep-learning",
        "artificial-intelligence",
        "latex",
        "neural-network",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    install_requires=[required_packages],
    extras_require={
        "dev": dev_packages,
    },
)
