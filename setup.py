from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='fastdb',
  version='0.0.8',
  entry_points = {
        'console_scripts': ['fastserver=fastdb.fastserver:run'],
  },
  project_urls = {
  'Github': 'https://www.github.com/kaankarakoc42/fastdb'
  },
  description='database for server-client jobs or local storage', 
  author='Mevlüt Kaan Karakoç',
  author_email='karakockaan326@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='database', 
  packages=find_packages(),
  install_requires=['flask','requests'] 
)
