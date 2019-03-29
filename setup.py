import setuptools

setuptools.setup(
    setup_requires=['pbr>=2.0.0', 'pytest-runner'],
    tests_require=['pytest', ],
    dependency_links=[
        'git+https://github.com/SD2E/python-datacatalog.git@2_0#egg=datacatalog'],
    pbr=True)
