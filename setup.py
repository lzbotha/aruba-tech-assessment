from setuptools import setup, find_packages

setup(
    name='aplocation',
    version='0.1.0',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[x.strip() for x in open('requirements.txt').readlines()],
    author='Leonard Botha',
    author_email='leonardzbotha@gmail.com',
    tests_require=["nose"],
    test_suite="nose.collector",
    include_package_data=True,
)