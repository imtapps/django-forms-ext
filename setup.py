from setuptools import find_packages
from distutils.core import setup

setup(
    name="django-forms-ext",
    version='1.1.0',
    author="IMT Computer Services",
    description="Extensions for Django's Forms.",
    long_description=open('README.txt', 'r').read(),
    url="http://github.com/imtapps/django-forms-ext",
    packages=find_packages(exclude=["example"]),
    install_requires=open('requirements/dist.txt').read().split("\n"),
    tests_requires=open('requirements/dev.txt').read().split("\n"),
    test_suite='runtests.runtests',
    zip_safe=False,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ]
)
