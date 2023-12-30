# Local GPT

This Python package enables private, context-aware retrieval augmented generation from your documents using Large Language Models (LLMs). It is essentially a reimplementation of [PrivateGPT](https://github.com/imartinez/privateGPT) with some simplifications. I developed this package both as a learning exercise in understanding LLMs and to facilitate their integration into my own projects.

## Overview
The primary purpose of this package is to provide a user-friendly interface for leveraging Large Language Models in a private and context-aware manner. It combines the power of retrieval and generation to enhance the utility of your documents.

## Features

- **Privacy**: The package ensures that the retrieval and generation processes are conducted in a private manner, safeguarding sensitive information.

- **Context Awareness**: The system considers context from your documents, allowing for more coherent and relevant generation.

- **Simplified Implementation**: Compared to its predecessor, this package offers a simplified implementation, making it easier to understand and use in your projects.

## Getting Started

1. Start by cloning the repository and installing the package dependencies:
    ```console
    git clone https://github.com/nikhil-ravi/localGPT
    cd localGPT

    conda create -n localGPT python=3.11
    conda activate localGPT
    poetry install
    ```
2. For GPU support, make sure to setup a C++ compiler, install the CUDA toolkit, verify installation with `nvcc --version` and `nvidia-smi`, and run the following command:  
For Linux:
    ```console
    CMAKE_ARGS='-DLLAMA_CUBLAS=on' poetry run pip install --force-reinstall --no-cache-dir llama-cpp-python
    ```
    For Windows:
    ```console
    $env:CMAKE_ARGS='-DLLAMA_CUBLAS=on'; poetry run pip install --force-reinstall --no-cache-dir llama-cpp-python
    ```
    For MacOS:
    ```console
    CMAKE_ARGS="-DLLAMA_METAL=on" pip install --force-reinstall --no-cache-dir llama-cpp-python
    ```
3. Modify the [`settings.yaml`](settings.yaml) file to point to your desired models.
4. To ease the installation process, use the setup script that will download both the embedding and the LLM model and place them in the correct location (under the models folder):
    ```console
    poetry run localGPT_setup
    ```
5. To start the program, run the following command:
    ```console
    poetry run python -m src.localGPT
    ```
6. Navigate to http://localhost:8001/docs in your browser to view the API documentation.
7. For the UI, navigate to http://localhost:8001/ in your browser.



## Acknowledgments

This package is inspired by the [PrivateGPT](https://github.com/imartinez/privateGPT) project. Special thanks to the contributors of that project.