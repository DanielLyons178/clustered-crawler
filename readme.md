# Scraper

Distributed and pluggable python web scraper

## TODO

- Restructure queuing
- Allow scaling engines
    - Write state of master engine to redis (exists)
    - Joining message sent to fanout exchange
    - Ouptput queue registrations to redis (from master engine) for addition of more engines