module.exports = {
  apps: [
    {
      name: "chronocast-frontend",
      script: "node_modules/.bin/vite",
      args: "preview --host",
      // Vite preview serves static files — fully stateless, cluster mode is safe
      instances: "max",
      exec_mode: "cluster",
      watch: false,
      autorestart: true,
      max_memory_restart: "500M",
      env: {
        NODE_ENV: "development",
      },
      env_production: {
        NODE_ENV: "production",
        PORT: 3000,
      },
      error_file: "logs/pm2-error.log",
      out_file: "logs/pm2-out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      merge_logs: true,
    },
  ],
};
