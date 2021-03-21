FROM python:3.8.8-alpine

COPY ./scraper/ /src/scraper

RUN pip install file:///src/scraper/scraper-common
RUN pip install file:///src/scraper/scraper-core

RUN rm -rf /src

ENTRYPOINT ["python", "-m", "scraper.core"]


