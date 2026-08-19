module.exports = {
  requires: {
    bundle: "ai",
  },
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        env: {
          DO_NOT_TRACK: "1",
          GRADIO_ANALYTICS_ENABLED: "False",
          HF_HUB_DISABLE_TELEMETRY: "1",
        },
        message: "python verify_install.py",
      },
    },
  ],
}
