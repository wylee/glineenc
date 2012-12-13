from distutils.core import setup


long_description = open('README').read()


setup(
    name='glineenc',
    version='1.1.dev0',
    description='Convert lat/long pairs to Base64 encoding for Google Maps',
    long_description=long_description,
    license='MIT',
    author='Wyatt Lee Baldwin',
    author_email='wyatt.lee.baldwin@gmail.com',
    keywords='Google Maps',
    url='https://bitbucket.org/wyatt/glineenc',
    packages=('glineenc', 'glineenc/tests'),
)
