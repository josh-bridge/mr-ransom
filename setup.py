from distutils.core import setup

setup(
    name='mrransom',
    version='0.1',
    packages=['', 'cipher'],
    package_dir={'': 'mrransom'},
    package_data={'package': "data/"},
    url='https://github.com/josh-bridge',
    license='',
    author='jbridgiee',
    author_email='14032908@stu.mmu.ac.uk',
    description='Python-based ransomware including custom encryption algorithm'
)
