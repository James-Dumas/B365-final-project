# B365-final-project

This project is a machine learning model designed to predict the final selling price of a smartphone auction listing on ebay.

This project consists of 3 parts:
1. Scraping data
1. Data processing
1. Prediction model

## Scraping data from ebay

Since viewing an auction's bid history requires being logged in, the scraper needs a logged in session to be able to work properly. The only way that I could find to do this is by exporting cookies from chrome using the [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid?hl=en) plugin after manually logging into an ebay account. Just place the exported file into the repo root before running the scraper. If everything runs smoothly it will output a new json file in the `data/scraped/` directory.

## Data Processing

## Prediction Model
