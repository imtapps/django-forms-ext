from setuptools import find_packages
from distutils.core import Command, setup
import os

from new_app import VERSION

REQUIREMENTS = [
    'django',
]

TEST_REQUIREMENTS = []

class InstallDependencies(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        all_dependencies = REQUIREMENTS + TEST_REQUIREMENTS
        os.system("pip install %s" % ' '.join(all_dependencies))

setup(
    name="django-new_app",
    version=VERSION,
    author="Author Name",
    author_email="author_email",
    description="Description for new_app.",
    long_description=open('README.txt', 'r').read(),
    url="http://www.example.com",
    packages=find_packages(exclude=["example"]),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS,
    test_suite='runtests.runtests',
    zip_safe=False,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    cmdclass={
        'install_dev': InstallDependencies,
    }
)
