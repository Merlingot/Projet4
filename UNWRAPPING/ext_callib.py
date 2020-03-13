from manta import ext_callib
import os


name='ext_manta_'
destination='/ext/'


if not os.isdir(destination):
    os.mkdir(destination)

ext_callib()
