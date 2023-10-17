# chat.mykal.codes

> [!WARNING]
> This is still a WIP! Please proceed with caution.

an LLM chatbot that ingests my blog posts, and lets you ask a digital me questions.

## Packages

| Package | Path                | Description                                               |
| ------- | ------------------- | --------------------------------------------------------- |
| API     | `/packages/api/`    | A Flask API that exposes the chat LLM                     |
| WebApp  | `/packages/webapp/` | An Astro site that puts a UI on top of the API 

## Getting Started

For a getting started guide, please see the README.md located in each package's folder.

Please note that while you can setup the API to operate by itself, the WebApp package relies on the API to function properly.