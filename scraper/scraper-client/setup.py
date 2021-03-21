from setuptools import setup


setup(
    name="scraper_client",
    version="1",
    description="Client package for scraper",
    author="Dan Lyons",
    author_email="daniel.lyons178@live.com",
    packages=[
        "scraper.client",
        "scraper.client.lib",
        "scraper.client.lib.link_extraction",
        "scraper.client.lib.body_reader",
    ],
    install_requires=["requests", "pika", "scraper-common"],
    zip_safe=False,
)