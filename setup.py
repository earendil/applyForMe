from setuptools import setup, find_packages


PACKAGES = find_packages(include="reedclient*")

setup_args = {
    'name': 'reedjobs',
    'version': "1.0.0",
    'license': 'Apache 2.0',
    'description': 'Python client for Reed API',
    'long_description': "",
    'url': '',
    'classifiers': ['Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers, job seekers, general public',
                    'Operating System :: POSIX',
                    'Topic :: Software Development :: Libraries',
                    'Programming Language :: Python :: 3.7'],
    'packages': PACKAGES,
    'install_requires': ['requests', 'selenium'],
}

setup(**setup_args)
