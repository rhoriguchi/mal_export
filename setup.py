from setuptools import setup, find_packages

setup(
    author='Ryan Horiguchi',
    author_email='ryan.horiguchi@gmail.com',
    dependency_links=[],
    entry_points={
        'console_scripts': ['mal_export = mal_export.__main__:main'],
    },
    install_requires=[
        'beautifulsoup4==4.9.0',
        'PyYAML==5.3.1',
        'requests==2.31.0'
    ],
    license='MIT',
    name='tv_time_export',
    packages=find_packages(),
    python_requires='>=3.7',
    url='git@github.com:rhoriguchi/mal_export.git',
    version='1.0.3',
    zip_safe=False,
)
