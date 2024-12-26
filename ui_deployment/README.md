<!-- markdownlint-disable MD026 -->

# Usage 🔧

This project is made for **Python 3.11** version.

> 👉 *You can delete this file before committing your project to GitHub.*

How to use this template project see the following steps:

1. Clone the project.
2. Build the Docker image locally (commands see below or in the Dockerfile).
3. Run the Docker container locally (commands see below or in the Dockerfile) and debug your streamlit app locally until you are ready to deploy to Streamlit Cloud.
4. Deploy the project to Streamlit Cloud and test it.

---

## Python **virtualenv** setup for local development 🐍

If you don't want to use Docker for local development, you can also use a Python virtual environment.
How to setup a Python virtual environment for local development:

### 1. Install virtualenv package

```bash
pip install --upgrade virtualenv
```

### 2. Make and activate virtual environment

```bash
python -m venv .venv
```

or

```bash
python3 -m venv .venv
```

#### On Windows

```bash
.venv\Scripts\activate
```

#### On macOS and Linux

```bash
source .venv/bin/activate
```

### 3. Install dependencies within the virtual environment

```bash
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

### 4. Develop and test your streamlit app within the virtual environment

```bash
streamlit run streamlit_app.py
```

### 5. After development, deactivate virtual environment

```bash
deactivate
```

---

## Dockerfile for local development 🐳

This template contains a Dockerfile for local debugging and testing of the project, before deploying the project to Streamlit Cloud. This shall ease the process of developing and deploying projects to Streamlit Cloud, without endless back and forth trial-and-error between local development environment, GitHub and Streamlit Cloud.

The Dockerfile is based on `python:3.11-slim` image and shall mimic the Streamlit Cloud runtime as closely as possible.

**Hint**: If you run the Dockerfile locally on a Windows host system, you have to uncomment the `[server]` settings in the `.streamlit/config.toml` file. Comment these lines again before deploying the project to Streamlit Cloud.

---

## Streamlit Cloud deployment ☁️

To deploy the project to Streamlit Cloud, you have to create a new project on Streamlit Cloud and connect it to your GitHub repository.
How to deploy a project to Streamlit Cloud see in the official documentation [here](https://docs.streamlit.io/streamlit-community-cloud).

---

## Resources 📚

See also the official documentation from Streamlit about docker deployments:

[https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
