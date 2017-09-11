from setuptools import setup

setup(
    name="pyrecipes",
    version="0.3",
    description="A collection of Python 3 functions and recipes for figure making.",
    author="Kelvin Lee",
    packages=["pyrecipes"],
    author_email="kin.long.kelvin.lee@gmail.com",
    install_requires=[
            "numpy",
            "pandas",
            "scipy",
            "peakutils",
            "seaborn",
            "colorlover",
            "matplotlib"
    ]
)
