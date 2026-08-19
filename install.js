const SOURCE_REPOSITORY = "https://github.com/FurkanGozukara/SUPIR"
const SOURCE_REVISION = "63b53ddb1773062ef64a4c192707f69d66b24953"

module.exports = {
  requires: {
    bundle: "ai",
  },
  run: [
    {
      when: "{{gpu !== 'nvidia' || !['win32', 'linux'].includes(platform)}}",
      method: "shell.run",
      params: {
        message: "python -c \"raise SystemExit('This SUPIR launcher requires an NVIDIA GPU on Windows or Linux.')\"",
      },
    },
    {
      method: "shell.run",
      params: {
        message: `git clone ${SOURCE_REPOSITORY} app`,
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
      when: "{{gpu === 'nvidia' && ['win32', 'linux'].includes(platform)}}",
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: [
          "uv pip install torch==2.5.1 torchvision==0.20.1 xformers==0.0.28.post3 --index-url https://download.pytorch.org/whl/cu124",
          "uv pip install -r requirements.txt",
          "uv pip install bitsandbytes==0.43.3 huggingface_hub==0.36.0",
        ],
      },
    },
    {
      when: "{{gpu === 'nvidia' && platform === 'win32'}}",
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "uv pip install https://github.com/woct0rdho/triton-windows/releases/download/v3.1.0-windows.post5/triton-3.1.0-cp310-cp310-win_amd64.whl",
      },
    },
    {
      when: "{{gpu === 'nvidia' && platform === 'linux'}}",
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "uv pip install triton==3.1.0",
      },
    },
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        env: {
          DO_NOT_TRACK: "1",
          GRADIO_ANALYTICS_ENABLED: "False",
          HF_HUB_DISABLE_TELEMETRY: "1",
        },
        message: "python -c \"import gradio, torch, transformers; print('torch', torch.__version__); print('cuda', torch.version.cuda); print('gradio', gradio.__version__); print('transformers', transformers.__version__)\"",
      },
    },
    {
      method: "notify",
      params: {
        html: "Dependencies installed. Download the required models before starting SUPIR.",
        type: "success",
      },
    },
  ],
}
