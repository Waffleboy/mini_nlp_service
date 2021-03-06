# Self Contained NLP Microservice

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

## What is this?

This is a NLP Microservice that can be rapidly deployed via Docker that does 3 main things once hosted:

1. Scrape a provided url and detect entities using standard NLP packages via `/scrape/{url}`.
   1. The default package uses `SpaCy` as it's the industry standard.
   2. [NOT ACTIVE - TODO] If it's a HTML page, by default the entire body will be scraped unless xpaths are specified via request param `xpaths_delimited_by_semicolon`. As many xpaths can be provided, seperated by a `;`. Currently the capability exists but is not yet implemented.
2. View all results currently in the database via `/entities`
3. View text with specific entities via `/entities/{entity}`

Built with FastAPI, The interactive docs are viewable at `/docs`. Documentation to the code available under `app/documentation`

Docker image built with FastAPI's optimized layer for responsiveness.

## Installation & Usage

### (Easiest) via GCP

Run via the google cloud button bove

### via Docker

```
git clone git@github.com:Waffleboy/mini_nlp_service.git
cd mini_nlp_service
docker build --no-cache -t mini_nlp_service .
docker run --name mini_nlp_service_container -p 80:80 mini_nlp_service

# navigate to the url where the docker instance is hosted (default: 0.0.0.0)
```
