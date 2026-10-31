# Qwen Kaggle API — Abliterated GGUF

A Strata-free Kaggle notebook for testing a Qwen3.8-Flash-Next abliterated GGUF with `llama.cpp`, then exposing the working server through an authenticated API and Cloudflare Tunnel.

## Status

**Bootstrap stage — not yet validated end-to-end on Kaggle.** The first milestone is to prove that a compatible `llama.cpp` build can load the selected GGUF on the available Kaggle GPU/RAM configuration. Do not assume the model fits just because the files are available.

## Quick start

1. Open `notebooks/Launch_API.ipynb` on GitHub.
2. In Kaggle, use **Copy & Edit** / import the notebook.
3. Enable Internet and a GPU accelerator.
4. Attach a Kaggle Dataset containing the model GGUF shards, or configure a Hugging Face download in the notebook.
5. Run the notebook from top to bottom. The initial notebook performs preflight checks and attempts to build `llama.cpp`; the API/tunnel stages are gated on a successful model load.

## Design

- **Inference:** upstream `llama.cpp`; no Strata runtime or Strata expert pack.
- **Model storage:** prefer a Kaggle Dataset mounted read-only under `/kaggle/input` to avoid duplicating multi-gigabyte files in `/kaggle/working`.
- **API:** OpenAI-compatible endpoints provided by `llama-server`.
- **Public access:** Cloudflare Tunnel, started only after local health checks pass.
- **Security:** use a randomly generated API key; never commit secrets or print the key in notebook output.
- **Persistence:** Kaggle Datasets can preserve files between sessions, but cannot preserve a live process. The server and tunnel must be restarted in each new session.

## Important constraints

- Kaggle's writable `/kaggle/working` volume is limited. Avoid copying a large GGUF into it.
- Available RAM + GPU memory may be insufficient for a 60+ GiB model. Memory mapping does not make the model's working set disappear; paging can make inference unusably slow.
- Qwen3.8-Flash-Next needs a `llama.cpp` revision that supports its architecture and quantization. The notebook records the selected revision and fails early if the build fails.
- A public tunnel is an internet-facing service. Keep API-key authentication enabled and do not expose an unauthenticated server.

## Repository layout

- `notebooks/Launch_API.ipynb` — Kaggle entry point.
- `scripts/preflight.py` — small environment and model-file checks.

## Roadmap

1. Validate model architecture/quantization support and model loading.
2. Validate authenticated local API requests.
3. Add Cloudflare Tunnel and external smoke test.
4. Add optional cache-dataset publishing/restoration and client configuration helpers.

This repository is experimental. A successful build is not proof that the model will fit or generate correctly on a given Kaggle accelerator.
