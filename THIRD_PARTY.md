# Third-party components

- The Python MCP package and its dependencies are installed through `pyproject.toml`; see each package's license.
- Codex CLI and Claude Code are installed into the Docker image by version, not vendored as source in this repository. Their original terms apply.
- DeepSeek Harness is developed by DeepSeek AI and distributed under the MIT license: https://github.com/deepseek-ai/deepseek-harness . Its pinned installation will accompany the new experiment runner.
- Hermes Agent is developed by Nous Research under the MIT license: https://github.com/NousResearch/hermes-agent . The Docker image installs version 0.21.2 at commit `b7b35a84b7fbe1aa2e223a6ce726a2471300d0a4`; upstream source is not vendored in this repository. Its source license stays inside the image.
- The paper directory contains ICLR 2027 LaTeX styles and supporting LaTeX packages, with their original notices preserved. These files do not imply conference acceptance or endorsement.

Original project material has no license grant in this initial public research snapshot.
