from setuptools import setup, find_packages

setup(
    name='multi-search-n-llm-image-downloader',
    version='0.1.0',
    author='Ishan',
    author_email='ishandutta2007@gmail.com',
    description='A package to download images from multiple search engines.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ishandutta2007/multi_search_n_llm_image_downloader',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'filetype',
        'requests',
        'selenium',
        'tqdm',
        'lxml',
        'chromedriver-autoinstaller',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'multi-search-n-llm-image-downloader=multidownloader:main',
        ],
    },
)
