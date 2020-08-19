# Evaluate a News Article with Natural Language Processing

The objective is to build a web tool that allows users to run Natural Language Processing (NLP) on articles or blogs found on other websites. NLP is the ability of an application to understand the human language, written or oral. NLPs leverage machine learning and deep learning create a program that can interpret natural human speech. Systems like Alexa, Google Assistant, and many voice interaction programs are well known to us, but understanding human speech is an incredibly difficult task and requires a lot of resources to achieve. Full disclosure, this is the Wikipedia definition:

> Natural language processing (NLP) is a subfield of computer science, information engineering, and artificial intelligence concerned with the interactions between computers and human (natural) languages, in particular how to program computers to process and analyze large amounts of natural language data.

You could spend years and get a masters degree focusing on the details of creating NLP systems and algorithms. Typically, NLP programs require far more resources than individuals have access to, but a fairly new API called MeaningCloud has put a public facing API in front of their NLP system. It is used in this project to determine various attributes of an article or blog post.

## Project Goal

The goal of this project is to practice with:
- Setting up Webpack
- Sass styles
- Webpack Loaders and Plugins
- Creating layouts and page design
- Service workers
- Using APIs and creating requests to external urls

## Getting started

`cd` into project root folder and run:
- `npm install`

## Setting up the API

### Step 1: Signup for an API key

You can find the API [here](https://www.meaningcloud.com/developer/sentiment-analysis). Once you create an account with MeaningCloud, you will be given a license key to start using the API.

### Step 2: Environment Variables

- [ ] Create a new ```.env``` file in the root of the project
- [ ] Fill the .env file with your API keys like this:
```
API_KEY=**************************
```

### Step 5: Using the API

We're ready to go! You can also check out the documentation of the MeaningCloud API [here](https://www.meaningcloud.com/developer/sentiment-analysis/doc/2.1).

## Running the Project

Run: `npm run build-prod` and then `npm run start`
