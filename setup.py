from setuptools import setup

setup( name='skcache'
     , version='0.1'
     , description='short description'
     , long_description='long description'
     , classifiers=[ 'Development Status :: 3 - Alpha'
                   , 'License :: OSI Approved :: MIT License'
                   , 'Programming Language :: Python :: 3.4' ]
     , keywords='sklearn cache'
     , url='https://github.com/whalebot-helmsman/scikit-cache'
     , author='Vostretsov Nikita'
     , author_email='whalebot.helmsman@gmail.com'
     , license='MIT'
     , packages=['skcache']
     , install_requires=['scikit-learn']
     , include_package_data=True
     , zip_safe=False )
