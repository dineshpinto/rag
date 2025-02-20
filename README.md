[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Flare](https://img.shields.io/badge/flare-network-e62058.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNCIgaGVpZ2h0PSIzNCI+PHBhdGggZD0iTTkuNC0uMWEzMjAuMzUgMzIwLjM1IDAgMCAwIDIuOTkuMDJoMi4yOGExMTA2LjAxIDExMDYuMDEgMCAwIDEgOS4yMy4wNGMzLjM3IDAgNi43My4wMiAxMC4xLjA0di44N2wuMDEuNDljLS4wNSAyLTEuNDMgMy45LTIuOCA1LjI1YTkuNDMgOS40MyAwIDAgMS02IDIuMDdIMjAuOTJsLTIuMjItLjAxYTQxNjEuNTcgNDE2MS41NyAwIDAgMS04LjkyIDBMMCA4LjY0YTIzNy4zIDIzNy4zIDAgMCAxLS4wMS0xLjUxQy4wMyA1LjI2IDEuMTkgMy41NiAyLjQgMi4yIDQuNDcuMzcgNi43LS4xMiA5LjQxLS4wOXoiIGZpbGw9IiNFNTIwNTgiLz48cGF0aCBkPSJNNy42NSAxMi42NUg5LjJhNzU5LjQ4IDc1OS40OCAwIDAgMSA2LjM3LjAxaDMuMzdsNi42MS4wMWE4LjU0IDguNTQgMCAwIDEtMi40MSA2LjI0Yy0yLjY5IDIuNDktNS42NCAyLjUzLTkuMSAyLjVhNzA3LjQyIDcwNy40MiAwIDAgMC00LjQtLjAzbC0zLjI2LS4wMmMtMi4xMyAwLTQuMjUtLjAyLTYuMzgtLjAzdi0uOTdsLS4wMS0uNTVjLjA1LTIuMSAxLjQyLTMuNzcgMi44Ni01LjE2YTcuNTYgNy41NiAwIDAgMSA0LjgtMnoiIGZpbGw9IiNFNjIwNTciLz48cGF0aCBkPSJNNi4zMSAyNS42OGE0Ljk1IDQuOTUgMCAwIDEgMi4yNSAyLjgzYy4yNiAxLjMuMDcgMi41MS0uNiAzLjY1YTQuODQgNC44NCAwIDAgMS0zLjIgMS45MiA0Ljk4IDQuOTggMCAwIDEtMi45NS0uNjhjLS45NC0uODgtMS43Ni0xLjY3LTEuODUtMy0uMDItMS41OS4wNS0yLjUzIDEuMDgtMy43NyAxLjU1LTEuMyAzLjM0LTEuODIgNS4yNy0uOTV6IiBmaWxsPSIjRTUyMDU3Ii8+PC9zdmc+&colorA=FFFFFF)](https://dev.flare.network/)

# Flare AI RAG

Flare AI Kit template for Retrieval-Augmented Generation (RAG) Knowledge.

## 🚀 Key Features

* **Modular Architecture**: Designed with independent components that can be easily extended.
* **Qdrant-Powered Retrieval**: Leverages Qdrant for fast, semantic document retrieval, but can easily be adapted to other vector databases.
* **Unified LLM Integration**: Supports over 300 models via OpenRouter, enabling flexible selection and integration of LLMs.
* **Highly Configurable & Extensible**: Uses a straightforward JSON configuration system, enabling effortless integration of new features and services.

## 📌 Prerequisites

Before getting started, ensure you have:

* A **Python 3.12** environment.
* [uv](https://docs.astral.sh/uv/getting-started/installation/) installed for dependency management.
* An [OpenRouter API Key](https://openrouter.ai/settings/keys).
* Access to one of the Flare databases. (The [Flare Developer Hub](https://dev.flare.network/) is included in CSV format for local testing.)

## 🏗️ Build & Run Instructions

You can deploy Flare AI RAG using Docker or set up the backend and frontend manually.

* **Environment Setup**: Rename `.env.example` to `.env` and add in the variables (e.g. your [OpenRouter API Key](https://openrouter.ai/settings/keys)).

### Build using Docker

* **Build the Docker Image**:

```bash
docker build -t flare-ai-rag .
```

* **Run the Docker Container**:

```bash
docker run -p 80:80 -it --env-file .env flare-ai-rag
```

### Build manually

* **Install Dependencies**: Install all required dependencies by running:

```bash
uv sync --all-extras
```

Verify your available credits and get all supported models with:

```bash
uv run python -m tests.credits
uv run python -m tests.models
```

* **Setup a Qdrant Service**: Make sure that Qdrant is up an running before running your script.
You can quickly start a Qdrant instance using Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

* **Configure Parameters and Run RAG**: The RAG consists of a router, a retriever, and a responder, all configurable within `src/input_parameters.json`.
Once configured, add your query to `src/query.txt` and run:

```bash
uv run start-rag
```

## 🔜 Next Steps & Future Upgrades

Design and implement a knowledge ingestion pipeline, with a demonstration interface showing practical applications for developers and users.
All code uses the TEE Setup which can be found in the [flare-ai-defai](https://github.com/flare-foundation/flare-ai-defai) repository.

_N.B._ Other vector databases can be used, provided they run within the same Docker container as the RAG system, since the deployment will occur in a TEE.

* **Enhanced Data Ingestion & Indexing**: Explore more sophisticated data structures for improved indexing and retrieval, and expand beyond a CSV format to include additional data sources (_e.g._, Flare’s GitHub, blogs, documentation). BigQuery integration would be desirable.
* **Intelligent Query & Data Processing**: Use recommended AI models to refine the data processing pipeline, including pre-processing steps that optimize and clean incoming data, ensuring higher-quality context retrieval. (_e.g._ Use an LLM to reformulate or expand user queries before passing them to the retriever, improving the precision and recall of the semantic search.)
* **Advanced Context Management**: Develop an intelligent context management system that:
  * Implements Dynamic Relevance Scoring to rank documents by their contextual importance.
  * Optimizes the Context Window to balance the amount of information sent to LLMs.
  * Includes Source Verification Mechanisms to assess and validate the reliability of the data sources.
* **Improved Retrieval & Response Pipelines**: Integrate hybrid search techniques (combining semantic and keyword-based methods) for better retrieval, and implement completion checks to verify that the responder’s output is complete and accurate (potentially allow an iterative feedback loop for refining the final answer).
