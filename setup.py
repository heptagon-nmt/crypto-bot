from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
    setup(
        name='yacu',
        version='0.0.3.5',
        author='Yet Another Crypto Util Team',
        author_email='',
        license='GPL3',
        description='Predict crypto prices with ML.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/1103s/crypto-bot',
        py_modules=['yacu', 'src'],
        packages=find_packages(),
        install_requires=[requirements],
        python_requires='>=3.6',
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Operating System :: OS Independent",
        ],
        entry_points={
            'console_scripts': [
                'yacu = yacu:gui',
                'yacu-cli = yacu:cli'
                ],
            },
    )
