# Ornith Heretic Kaggle API

[![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/seczoid/qwen-kaggle-api-abliterated/blob/master/notebooks/Launch_API.ipynb)

A minimal Kaggle notebook that downloads a quantized **Ornith-1.5-9B Heretic** GGUF, builds upstream `llama.cpp`, starts an authenticated OpenAI-compatible API, and optionally exposes it through a Cloudflare Quick Tunnel.

## Quick start

1. Click **Open in Kaggle** above.
2. In Kaggle settings, enable **Internet** and a **GPU accelerator**.
3. Run the notebook from top to bottom. It downloads the model automatically; no Kaggle Dataset attachment is required.

## Model choice

Default: `Thunder13240/Ornith-1.5-9B-heretic-GGUF` — `Ornith-1.5-9B-heretic-IQ4_XS.gguf` (about 5.2 GB). This is a practical quality/size starting point for Kaggle's T4-class GPU options. The upstream model card reports favorable size/quality results for IQ4_XS, but published tokens-per-second figures are hardware-specific; actual Kaggle throughput must be measured on the allocated accelerator. For text-only chat, the vision projector file is not needed.

To try another quant, change `MODEL_FILENAME` in the configuration cell to an exact GGUF filename from the [model repository](https://huggingface.co/Thunder13240/Ornith-1.5-9B-heretic-GGUF).

## Design and constraints

- **Inference:** upstream `llama.cpp`; no Strata runtime or expert-pack generation.
- **Model download:** public Hugging Face file downloaded into `/kaggle/working/models`; Kaggle Internet must be enabled.
- **API:** OpenAI-compatible endpoints provided by `llama-server`.
- **Public access:** optional Cloudflare Quick Tunnel, started only after local health and chat-completion checks pass.
- **Security:** the server uses a randomly generated API key. Keep it private; do not use this experimental endpoint for sensitive data.
- **Session lifetime:** the server and Quick Tunnel stop when the Kaggle session ends. The tunnel URL changes when restarted.

## Notes

- Kaggle resource allocations vary. A successful build does not guarantee the model loads or achieves a particular tokens-per-second rate.
- The notebook has not yet been validated end-to-end on a live Kaggle session.
- If the CUDA build fails, capture the full CMake error before changing compiler or CUDA settings.
