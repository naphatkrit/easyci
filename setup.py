from setuptools import setup, find_packages

tests_require = [
    'flake8>=2.4.0',
]

install_requires = [
    'Click>=5.0',
]

setup(
    name='easyci',
    version='0.1',
    author='Naphat Sanguansin',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={'tests': tests_require},
    tests_require=tests_require,
    entry_points='''
        [console_scripts]
        eci=easyci.cli:cli
    ''',
)
