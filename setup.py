from setuptools import setup, find_packages

setup(
    name='OpenAIChat',
    version='0.1.0',
    author='jeffreyc2017',
    author_email='',
    description='A chat application powered by OpenAI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jeffreyc2017/openai-chat',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'openai',
        'tiktoken',
        'requests',
        'beautifulsoup4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'openaichat=OpenAIChat.main:main',
        ],
    },
)