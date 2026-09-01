from pathlib import Path
from setuptools import setup

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name='ethiocalendar',
    packages=['ethiocalendar'],
    version='1.2.0',
    license='MIT',
    description='Ethiopian Calendar based date and time module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mukerem Ali',
    author_email='mukeremali112@gmail.com',
    url='https://github.com/mukerem/ethiocalendar',
    download_url='https://github.com/mukerem/ethiocalendar/archive/refs/tags/v1.2.0.tar.gz',
    python_requires='>=3.6',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)
