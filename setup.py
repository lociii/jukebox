import ez_setup
import glob
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name="jukebox",
    packages=find_packages(),
    version="0.1.0",
    description="Jukebox - your democratic music player",
    author="Jens Nistler",
    author_email="opensource@jensnistler.de",
    url="https://jensnistler.de/jukebox",
    download_url='http://github.com/lociii/jukebox',
    keywords=["jukebox", "music", "mp3"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Players",
    ],
    install_requires=[
        "Django==1.3",
        "mutagen==1.20",
        "django-social-auth==0.6.0",
        "djangorestframework==0.2.3",
        "python-shout==0.2",
        "python-daemon==1.6",
    ],
    include_package_data=True,
    scripts=glob.glob("bin/*")
)
