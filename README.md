# RAG-APP

This is RAG Application and in this project we will Software Engineering and Data Science &amp; AI, we will show and highlight the importance of Software Engineering Skills in Data Science and AI Projects to be ready to production.


## Requirements

- Python 3.12 or Later


## Installation

1) Download and Install MiniConda from [here](https://docs.conda.io/en/latest/miniconda.html)

2) Create a Veritual Envirements

```bash
conda create -n rag_app python=3.12
```

3) Activate the Veritual Eniveroment

```bash
conda activate rag_app
```

3) Install the required packages

```bash
pip install -r requirements.txt
```

### Setup the environment variables
```bash
$ cp the .env.example file to .env and fill in the values
```


### Run the application

```bash
uvicorn src.main:app --reload
```


