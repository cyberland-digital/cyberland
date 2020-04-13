from setuptools import setup, find_packages

setup(
    name='flaskr',
    version='1.0.0',
    license='MIT',
    author='James Stone',
    author_email='jstone@jnet-it.com',
    description='Flask application powering cyberland.digital',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
