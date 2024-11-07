from setuptools import find_packages, setup

setup(
    name='elixir',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'PyYAML==6.0.2',
        'easydict==1.13',
    ],
    extras_require={
        'core': [
            'redis==5.0.1',
            'apispec==6.7.1'
            'Flask==3.0.3',
            'Flask-WTF==1.2.1',
            'Flask-HTMX==0.4.0',
            'Flask-Caching==2.3.0',
            'msgpack==1.1.0',
            'greenstalk==2.0.2',
            'pydantic==2.9.2',
            'click==8.1.7',
            'colorlog==6.8.0',
            'cryptography==41.0.7',
        ],
        'db': [
            'peewee==3.17.7',
            'mysqlclient==2.2.1',
            'psycopg2==2.9.9',
        ],
        'plugins': [
            'Flask==3.0.3',
            'Flask-WTF==1.2.1',
            'Flask-Login==0.6.3',
            'peewee==3.17.7',
            'qrcode==8.0',
            'pyotp==2.9.0',
        ],
        'all': [
            'elixir[web]',
            'elixir[db]',
            'elixir[plugins]',
        ],
    },
    author='Wireless Logic Benelux',
    description='Elixir: Core utilities, database models, and plugins for Flask applications',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)