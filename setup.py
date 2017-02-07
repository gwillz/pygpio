#!/usr/bin/env python

from setuptools import setup
import os, glob

requirements = [i for i in open('requirements.txt').read().split('\n') if not i.startswith('--') and len(i) > 0]

def get_long_description(fname):
    try:
        import pypandoc
        return pypandoc.convert(fname, 'rst')
    except:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='pygpio',
      version='0.1',
      description="An abstract interface for GPIO libraries",
      long_description=get_long_description('README.md'),
      author='Gwilyn Saunders',
      author_email='gwilyn.saunders@mk2es.com.au',
      url='https://git.mk2es.com/mk2/pygpio',
      packages=['pygpio'],
      install_requires=requirements,
      classifiers=[
          'Operating System :: POSIX',
          'Operating System :: POSIX :: BSD',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4'
      ]
)
