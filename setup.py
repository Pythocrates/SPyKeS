'''This is the SPyKeS package. It provides simple key storage capabilities.'''

from setuptools import find_packages, setup

setup(
    name='spykeys',
    author='Pythocrates',
    author_email='23015037+Pythocrates@users.noreply.github.com',
    url='https://github.com/Pythocrates/SPyKeS',
    description=__doc__,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    use_scm_version=True,
    setup_requires=['setuptools_scm>=3.3.3'],
    packages=find_packages(),
    install_requires=[
        'GitPython>=3.1.7',
        'python-gnupg>=0.4.6',
    ],
    tests_require=[
        'pytest>=6.0.1',
    ],

    entry_points={
        'console_scripts': ['spk = spykes.spk:main']
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
