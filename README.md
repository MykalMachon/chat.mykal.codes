# chat.mykal.codes

An LLM-Powered guide to mykal.codes

## Introduction

This project leverages a Large Language Model (LLM) combined with a Retrieval-Augmented Generation (RAG) pipeline to facilitate conversations about content from my blog [mykal.codes](https://mykal.codes/). In practice, this allows users to interact with a bot that serves as an 'expert' on my blog, referencing and synthesizing information across multiple posts.

## Inspiration

I find the concept of "natural" computing interfaces exciting. Actually *talking* to a computer and having it respond intelligently in natural language still blows my mind a bit.I’m interested in testing how well an LLM equipped with content I wrote can *accurately* reflect my views and engage users in meaningful discussions.

## Strengths 

- **Summarizing overarching themes on the site**: I think the bot does a pretty solid job of summarizing both individual posts and overarching themes. Try asking it what I think of docker, or what I like about coffee for examples of this.
- **Connecting multiple posts on similar topics**: In testing the app, I've noticed it's great at suggesting posts that relate to the current topic of conversation. For example, when discussing Docker, it might suggest posts about devops or orchestration.
- **A fun way to browse the site**: Chat bots like this are a fun alternative ways to browse the site as opposed to just scrolling through my posts archive. 

## Architectural Components

- **Web app**: The user interface for this app is a client-side web app built with Svelte, served by the Astro web server. It handles user interactions and displays the chat interface.
- **Web server**: This component serves the web app and acts as a simple API gateway to the Langbase services.
- **Langbase Pipe RAG agent**: At the core of the RAG/LLM pipeline, this agent handles querying the LLM, embedding content for efficient retrieval, and monitoring/logging activities. It simplifies the process of fetching content and generating coherent responses using the LLM of your choice.


### History 

In earlier version of chat.mykal.codes, The RAG pipeline was built into a Flask API service that would fetch my posts, create a vector store and embeddings, then request completions with the OpenAI API directly. *I was able to completely replace this custom component with a Langbase Pipe.*

I moved to Langbase as it's been on my radar for awhile. It significantly streamlined the process of incorporating my blogs content into the pipelines and reduced the overhead of maintaining this app.