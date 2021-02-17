import setuptools

setuptools.setup(
    name="scraper-core-DanLyons", # Replace with your own username
    version="0.0.1",
    author="Dan Lyons",
    author_email="daniel.lyons178@live.com",
    description="A distributed scraper",
    long_description="TODO",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=["requests","pika","redis"],
    python_requires='>=3.6',
)