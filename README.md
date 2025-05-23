# docsumma

Document summarization

## Configuration File

Rename the configuration file `config.cfg_example` to `config.cfg` and set the parameters with location of the files.

```
[FILES]
input_dir = data/in
output_dir = data/out
md_dir = data/md
```

It's strongly recommended to keep the default model to `granite3.1-dense:8b` (IBM) for the summarization.

## Dependencies

On Windows, install Python 3.11

```
PS C:\Users\marce\Work\docsumma> winget install Python.Python.3.11
```

> Note: The software stack is very senstive to the versioning of the libraries. One should be conservative with the versions that are installed.

Install [Ollama](https://ollama.com/download) for your platform like Windows or Linux. It's necessary to the embedding model:

```
(venv) PS C:\Users\marce\Work\docsumma> ollama pull nomic-embed-text
```


Activate the environment and install the dependencies. Be patient, it takes a while to install all the dependencies.

```
(venv) PS C:\Users\marce\Work\docsumma> cat .\requiments.txt
langchain>=0.1.0
langchain-community>=0.0.13
langchain-core>=0.1.17
langchain-ollama>=0.0.1
pdfminer.six>=20221105
markdown>=3.5.2
docling>=2.0.0
beautifulsoup4>=4.12.0
unstructured>=0.12.0
chromadb>=0.4.22
faiss-cpu>=1.7.4
(venv) PS C:\Users\marce\Work\docsumma>
(venv) PS C:\Users\marce\Work\docsumma> pip install -r .\requiments.txt
```

### Developer Mode

On Windows is necessary to habilitate the developer mode in the _Settings_.

```
System -> For developers -> Developer mode
```

## Running the code

Run the code

```
(venv) PS C:\Users\marce\Work\docsumma> python .\docsumma.py
Converting document: data\in\01-00-00-002-0001_KAUST_BYLAWS_10-25-06.pdf
Starting conversion...
(...)
```

## Models

Testing different models to compare the summarization of them:

* [granite3.1-dense:8b](https://ollama.com/library/granite3.1-dense) (IBM)
* [Phi4 (14b)](https://ollama.com/library/phi4) (Microsoft)
* [llama3.2-vision (11b)](https://ollama.com/library/llama3.2-vision) (Meta)



