from setuptools import setup, find_packages

setup(
    name = 'DFServer',
    version = '0.0.1',
    packages=find_packages(include=["DFServer","DFServer.*"]),
    include_package_data=True,
    package_data={
        "DFServer":[
            "DFBaseServer.py",
            "screens_generic/*.html",
            "static/*.*",
            "static/js/*.*",
            "static/fonts/*.*",
            "templates/totem.html"]
    },
    exclude_package_data={
        "DFServer":["test_t*.py"]
    },
    install_requires=[
        'flask','flask-socketio'
    ]
)