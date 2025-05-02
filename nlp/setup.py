from setuptools import setup, find_packages

setup(
    name="faq_classifier",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "transformers",
        "torch",
        "matplotlib",
        "seaborn",
        "joblib"
    ]
) 