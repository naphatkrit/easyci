from setuptools import setup, find_packages

tests_require = [
    'flake8>=2.4.0',
    'pytest>=2.5.0',
    'mock>=1.0.0',
]

install_requires = [
    'Click>=5.0',
    'PyYAML>=3.11',
]

setup(
    name='easyci',
    version='0.4.0',
    author='Naphat Sanguansin',
    author_email='naphat.krit@gmail.com',
    description='Local CI, for mortals.',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'easyci': ['hooks/*'],
    },
    install_requires=install_requires,
    extras_require={'tests': tests_require},
    url='https://github.com/naphatkrit/easyci',
    download_url='https://github.com/naphatkrit/easyci/tarball/0.4.0',
    tests_require=tests_require,
    entry_points='''
        [console_scripts]
        eci=easyci.cli:cli
    ''',
)
