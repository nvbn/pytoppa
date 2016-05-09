from setuptools import setup, find_packages

setup(
    name='pytoppa',
    version='15.0.2',
    description="Easy to use publisher of python packages to ppa",
    long_description="""\
""",
    classifiers=[],
    keywords='',
    author='Vladimir Iakovlev',
    author_email='nvbn.rm@gmail.com',
    url='https://github.com/nvbn/pytoppa',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={
        '': ['*.tmpl'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'PyYAML',
        'Jinja2',
    ],
    entry_points={
        'gui_scripts': [
            'pytoppa=pytoppa.app:main',
        ]
    },
)
