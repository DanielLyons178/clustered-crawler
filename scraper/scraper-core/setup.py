from setuptools import setup


setup(
    name="scraper_core",
    version="0.1.0",
    description="Core package for scraper",
    author="Dan Lyons",
    author_email="daniel.lyons178@live.com",
    packages=[
        "scraper.core",
        "scraper.core.engine",
        "scraper.core.engine.comms",
        "scraper.core.engine.comms.redis",
        "scraper.core.engine.comms.output",
        "scraper.core.engine.visitor",
    ],
    install_requires=["requests", "pika", "scraper-common", "redis"],
    zip_safe=False,
)