const SOURCE_REVISION = "63b53ddb1773062ef64a4c192707f69d66b24953"

module.exports = {
  version: "1.0.1",
  title: "SUPIR v100",
  description: "Pinned, privacy-conscious Pinokio launcher for SUPIR photo restoration.",
  menu: async (kernel, info) => {
    const installed = info.exists("app/env") && info.exists("app/gradio_demo.py")
    const modelsReady = [
      "app/models/v0Q.ckpt",
      "app/models/llava-v1.5-7b/config.json",
      "app/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
    ].every((file) => info.exists(file))
    const running = {
      install: info.running("install.js"),
      models: info.running("download-models.js"),
      start: info.running("start.js"),
      update: info.running("update.js"),
      verify: info.running("verify.js"),
      reset: info.running("reset.js"),
    }

    if (running.install) {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Installing Dependencies",
        href: "install.js",
      }]
    }

    if (running.models) {
      return [{
        default: true,
        icon: "fa-solid fa-download",
        text: "Downloading Required Models",
        href: "download-models.js",
      }]
    }

    if (running.start) {
      const local = info.local("start.js")
      const menu = []
      if (local && local.url) {
        menu.push({
          default: true,
          icon: "fa-solid fa-rocket",
          text: `Open Web UI - ${local.mode || "SUPIR"}`,
          href: local.url,
        })
      }
      menu.push({
        default: menu.length === 0,
        icon: "fa-solid fa-terminal",
        text: "Terminal",
        href: "start.js",
      })
      return menu
    }

    if (running.update || running.verify || running.reset) {
      const active = running.update
        ? ["Updating", "update.js"]
        : running.verify
          ? ["Verifying", "verify.js"]
          : ["Resetting", "reset.js"]
      return [{
        default: true,
        icon: "fa-solid fa-terminal",
        text: active[0],
        href: active[1],
      }]
    }

    if (!installed) {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Install Dependencies",
        href: "install.js",
      }]
    }

    if (!modelsReady) {
      return [
        {
          default: true,
          icon: "fa-solid fa-download",
          text: "Download Required Models (~48.31 GiB)",
          href: "download-models.js",
        },
        {
          icon: "fa-solid fa-rotate",
          text: "Update Launcher",
          href: "update.js",
        },
        {
          icon: "fa-regular fa-circle-xmark",
          text: "Reset",
          href: "reset.js",
          confirm: "Delete the installed source, Python environment, models, and cache?",
        },
      ]
    }

    return [
      {
        default: true,
        icon: "fa-solid fa-power-off",
        text: "Start - Balanced (FP16/BF16)",
        href: "start.js",
        params: {
          mode: "Balanced (FP16/BF16)",
        },
      },
      {
        icon: "fa-solid fa-memory",
        text: "Start - Low VRAM (FP8)",
        href: "start.js",
        params: {
          mode: "Low VRAM (FP8)",
        },
      },
      {
        icon: "fa-solid fa-gauge-high",
        text: "Start - Full Precision",
        href: "start.js",
        params: {
          mode: "Full Precision",
        },
      },
      {
        icon: "fa-solid fa-circle-check",
        text: "Verify Installation",
        href: "verify.js",
      },
      {
        icon: "fa-solid fa-download",
        text: "Resume or Verify Model Download",
        href: "download-models.js",
      },
      {
        icon: "fa-solid fa-rotate",
        text: `Update Launcher (SUPIR stays at ${SOURCE_REVISION.slice(0, 8)})`,
        href: "update.js",
      },
      {
        icon: "fa-regular fa-circle-xmark",
        text: "Reset",
        href: "reset.js",
        confirm: "Delete the installed source, Python environment, models, and cache?",
      },
    ]
  },
}
