module.exports = {
  requires: {
    bundle: "ai",
  },
  run: [
    {
      method: "shell.run",
      params: {
        venv: "app/env",
        env: {
          DO_NOT_TRACK: "1",
          HF_HUB_DISABLE_TELEMETRY: "1",
          HF_HUB_ENABLE_HF_TRANSFER: "0",
        },
        message: "python download_models.py",
      },
    },
    {
      method: "notify",
      params: {
        html: "Required SUPIR models are downloaded and pinned to the tested revision.",
        type: "success",
      },
    },
  ],
}
