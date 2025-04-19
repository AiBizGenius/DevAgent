# 🤖 GitHub Actions Agent – CI/CD Workflow Generator

An AI-powered agent that dynamically generates GitHub Actions workflows based on configuration fetched from the GROQ API. Automate your CI/CD pipelines with secure, modular, and intelligent DevOps tooling.

---

## ✨ Features

- ⚙️ **Dynamic Workflow Generation** – Automatically creates GitHub Actions CI/CD YAML files.
- 🔌 **GROQ API Integration** – Fetches real-time configuration for workflows.
- 🐍 **Python & Docker Support** – Full pipeline including environment setup, dependency management, and container testing.
- 🔐 **Secure Secrets Management** – Injects API keys and tokens via GitHub Secrets.
- 🧪 **Automated Endpoint Testing** – Validates deployed containers by testing served endpoints.
- 🚀 **Efficient & Cached Builds** – Uses pip caching for faster build times.
- 🧩 **Modular & Extensible Design** – Clean separation of logic using Pydantic and custom agents.

---

## 🧰 Tech Stack

- `Python`
- `GitHub Actions`
- `Docker`
- `Pydantic`
- `GROQ API`

---

## 🧠 How It Works

1. **Configure the Agent**

   Define settings using the `GitHubActionsConfig` model – including workflow name, Python version, and GROQ API credentials.

2. **Initialize the Agent**

   Create an instance of `GitHubActionsAgent` with the configuration.

3. **Fetch Config from GROQ**

   The agent retrieves updated workflow configuration via the GROQ API.

4. **Generate the Workflow**

   Call `generate_pipeline()` to get a full `.yml` workflow file, ready to be used in your repository.

---

## 🔒 Secrets Setup (Required)

Before using the generated workflow, set the following secrets in your GitHub repo:

| Secret Name           | Description                     |
|-----------------------|---------------------------------|
| `GROQ_API_ENDPOINT`   | GROQ API endpoint URL           |
| `GROQ_API_KEY`        | Your GROQ API authentication key |
| `GH_TOKEN`            | GitHub Personal Access Token     |

---

## 📂 Directory Structure

