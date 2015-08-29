from setuptools import setup, find_packages

import easyci


tests_require = [
    'flake8>=2.4.0',
    'pytest>=2.5.0',
    'mock>=1.0.0',
]

install_requires = [
    'Click>=5.0',
    'PyYAML>=3.11',
    'subprocess32>=3.2.6',
]

setup(
    name='easyci',
    version=easyci.__version__,
    author='Naphat Sanguansin',
    author_email='naphat.krit@gmail.com',
    description='Local CI, for mortals.',
    packages=find_packages(),
    package_data={
        'easyci.hooks': ['*'],
    },
    install_requires=install_requires,
    extras_require={'tests': tests_require},
    url='https://github.com/naphatkrit/easyci',
    download_url='https://github.com/naphatkrit/easyci/tarball/' + easyci.__version__,
    tests_require=tests_require,
    keywords=['continuous', 'integration', 'easy', 'ci',
              'gating', 'tests', 'testing', 'test', 'git'],
    entry_points='''
        [console_scripts]
        eci=easyci.cli:cli
    ''',
)
