from setuptools import setup

setup(
    name='mtls_poc',
    version='1.0.0',
    author='Jefferson Silva',
    description='Poc conexão mtls com socket',
    packages=['mtls_poc'],
    install_requires=[
        'pytest',
    ],
    python_requires='>=3.8',
)
