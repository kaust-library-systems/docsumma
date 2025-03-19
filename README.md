# docsumma

Document summarization


## TODO

- [X] Test different models.
- [X] Directories for Markdown and the text with answered questions
- [ ] Create a log file.
- [ ] Log the files that failed in the process.


## Dependencies

Installing dependencies for Ollama and Python packages


```
ollama pull granite3.1-dense:8b
ollama pull nomic-embed-text
```

```
pip install -q `
"langchain>=0.1.0" `
"langchain-community>=0.0.13" `
"langchain-core>=0.1.17" `
"langchain-ollama>=0.0.1" `
"pdfminer.six>=20221105" `
"markdown>=3.5.2" `
"docling>=2.0.0" `
"beautifulsoup4>=4.12.0" `
"unstructured>=0.12.0" `
"chromadb>=0.4.22" `
"faiss-cpu>=1.7.4" `
"requests>=2.32.0" `
"IPython"
```

> _Note_: the `pip` command above is with Powershell syntax.

> _Note 2:_ Marked the windows dependency in `requiments.txt`<br>
> `pywin32==307; platform_system=="Windows"`

## Libraries

Maybe it's necessary to [match the CUDA library with the other libraries](https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/) - specially PyTorch by setting an environment variable

```
(docsumma) mgarcia@ilmen:~/Work/docsumma$ echo $TORCH_CUDA_ARCH_LIST
7.0 7.5 8.0 8.9
(docsumma) mgarcia@ilmen:~/Work/docsumma$
```

I also removed the library `ninja` from the dependencies and system.

## Models

Testing different models to compare the summarization of them:

* [granite3.1-dense:8b](https://ollama.com/library/granite3.1-dense) (IBM)
* [Phi4 (14b)](https://ollama.com/library/phi4) (Microsoft)
* [llama3.2-vision (11b)](https://ollama.com/library/llama3.2-vision) (Meta)

## Docker

Using [Docker Ollama](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image) image with NVIDIA GPU:

1. Install the [Nvidia container toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation).
1. Run Ollama inside a Docker container.

```
mgarcia@ilmen:~/Work$ docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama
/ollama
a5f1c9b16e086e5b587be364507b7e424bb27bc43097ff9b6b13e7e615269cec                                          
mgarcia@ilmen:~/Work$ docker exec -it ollama ollama run llama2                                            
pulling manifest 
(...)
```

For example, after downloading a few models:

```
mgarcia@ilmen:~/Work$ docker exec -it ollama ollama list
NAME                       ID              SIZE      MODIFIED
nomic-embed-text:latest    0a109f422b47    274 MB    20 seconds ago
granite3.1-dense:latest    34d3be74ec54    5.0 GB    25 minutes ago
phi4:latest                ac896e5b8b34    9.1 GB    37 minutes ago
llama2:latest              78e26419b446    3.8 GB    43 minutes ago
mgarcia@ilmen:~/Work$
```


