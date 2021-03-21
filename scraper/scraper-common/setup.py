from setuptools import setup


setup(
    name="scraper_common",
    version="0.1.0",
    description="Common utility package for scraper",
    author="Dan Lyons",
    author_email="daniel.lyons178@live.com",
    packages=["scraper.common.comms.rabbit"],
    zip_safe=False,
)