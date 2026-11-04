# Ornith Heretic Kaggle API

[![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/seczoid/qwen-kaggle-api-abliterated/blob/master/notebooks/Launch_API.ipynb)

A minimal Kaggle notebook that downloads a quantized **Ornith-1.5-9B Heretic** GGUF, builds upstream `llama.cpp`, starts an authenticated OpenAI-compatible API, and optionally exposes it through a Cloudflare Quick Tunnel.

## Quick start

1. Click **Open in Kaggle** above.
2. In Kaggle settings, enable **Internet** and a **GPU accelerator**.
3. Run the notebook from top to bottom. It downloads the model automatically; no Kaggle Dataset attachment is required.

## Model selection

Default: [`Thunder13240/Ornith-1.5-9B-heretic-GGUF`](https://huggingface.co/Thunder13240/Ornith-1.5-9B-heretic-GGUF), file `Ornith-1.5-9B-heretic-IQ4_XS.gguf` (about 5.20 GB). IQ4_XS is a good starting point for balancing model quality and memory use on a constrained GPU. The repository's published speed figures are hardware-specific and should not be treated as Kaggle performance claims.

To change quantization, set `MODEL_FILENAME` in the notebook configuration to an exact filename listed on the Hugging Face model page. The default is text-only; the optional vision projector is not downloaded.

## What the notebook does

1. Downloads the selected GGUF from Hugging Face into `/kaggle/working/models`.
2. Clones and builds upstream `llama.cpp` with CUDA, including a CUDA driver-stub hint for Kaggle runtimes that fail to expose `CUDA::cuda_driver` automatically.
3. Starts `llama-server` with a random API key.
4. Tests the local OpenAI-compatible chat-completions endpoint.
5. Starts a Cloudflare Quick Tunnel only after the local checks pass.

## Constraints and safety

- Enable Kaggle Internet and a GPU accelerator before running.
- The notebook and public tunnel work only while the Kaggle session remains alive. Quick Tunnel URLs change on restart.
- Resource allocations vary; a successful build does not guarantee the model fits or achieves a particular tokens/sec rate.
- Keep the generated API key private. Anyone with the public tunnel URL and API key may be able to use the endpoint. Do not use this experimental endpoint for sensitive data.
- The notebook is a best-effort launcher and still requires an end-to-end Kaggle run to validate the current runtime's CUDA configuration and model loading.

## Repository layout

- `notebooks/Launch_API.ipynb` — Kaggle launcher.
- `scripts/preflight.py` — legacy standalone preflight helper; not required by the notebook.
