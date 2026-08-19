module.exports = {
  requires: {
    bundle: "ai",
  },
  daemon: true,
  run: [
    {
      method: "local.set",
      params: {
        mode: "{{input.mode || 'Balanced (FP16/BF16)'}}",
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
          PYTHONWARNINGS: "ignore",
          TOKENIZERS_PARALLELISM: "false",
        },
        message: "python gradio_demo.py --ip 127.0.0.1 --port {{port}} --outputs_folder_button {{local.mode === 'Low VRAM (FP8)' ? '--loading_half_params --fp8 --use_tile_vae' : (local.mode === 'Full Precision' ? '--dont_move_cpu' : '--loading_half_params --use_tile_vae')}}",
        on: [
          {
            event: "/Running on local URL:\\s+(http:\\/\\/[0-9.:]+)/i",
            done: true,
          },
          {
            event: "/error:/i",
            break: false,
          },
        ],
      },
    },
    {
      method: "local.set",
      params: {
        url: "{{input.event[1]}}",
      },
    },
  ],
}
