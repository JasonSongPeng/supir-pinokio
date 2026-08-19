const SOURCE_REVISION = "63b53ddb1773062ef64a4c192707f69d66b24953"

module.exports = {
  requires: {
    bundle: "ai",
  },
  run: [
    {
      method: "shell.run",
      params: {
        message: "git pull --ff-only",
      },
    },
    {
      method: "shell.run",
      params: {
        path: "app",
        message: `git checkout --detach ${SOURCE_REVISION}`,
      },
    },
    {
      method: "shell.run",
      params: {
        message: "python configure_source.py",
      },
    },
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: [
          "uv pip install -r requirements.txt",
          "uv pip install bitsandbytes==0.43.3 huggingface_hub==0.36.0",
        ],
      },
    },
  ],
}
