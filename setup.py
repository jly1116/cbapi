'''
@time: 08-28-2020
@author: Leyuan Jiang
'''

from setuptools import setup

setup(

    name="cbapi",
    author="Leyuan Jiang",
    packages=["cbapi"],
    version="1.0",
    description="CrunchBase data API, retrieve organization & people data based on RapidAPI",
    install_requires=['json','requests','pandas','threading','queue','datetime']

)