import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from "chart.js"
import { Bar, Doughnut, Line } from "react-chartjs-2"

import { useDashboardData } from "./hooks/useDashboardData"

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  Filler,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
)

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
})

const numberFormatter = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 2,
})

const chartOptions = {
  maintainAspectRatio: false,
  interaction: { intersect: false, mode: "index" },
  plugins: {
    legend: {
      labels: {
        color: "#d6e5ff",
      },
    },
  },
  scales: {
    x: {
      grid: {
        color: "rgba(148, 163, 184, 0.08)",
      },
      ticks: {
        color: "#94a3b8",
      },
    },
    y: {
      grid: {
        color: "rgba(148, 163, 184, 0.08)",
      },
      ticks: {
        color: "#94a3b8",
      },
    },
  },
}

function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "N/A"
  }
  return currencyFormatter.format(value)
}

function formatNumber(value, suffix = "") {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "N/A"
  }
  return `${numberFormatter.format(value)}${suffix}`
}

function MetricCard({ eyebrow, title, value, detail, tone = "emerald" }) {
  const toneClass = {
    emerald: "from-emerald-400/20 via-emerald-400/5 to-transparent text-emerald-200",
    cyan: "from-cyan-400/20 via-cyan-400/5 to-transparent text-cyan-200",
    amber: "from-amber-400/20 via-amber-400/5 to-transparent text-amber-200",
    rose: "from-rose-400/20 via-rose-400/5 to-transparent text-rose-200",
  }[tone]

  return (
    <div className={`glass-card relative overflow-hidden p-6`}>
      <div className={`absolute inset-0 bg-gradient-to-br ${toneClass}`} />
      <div className="relative">
        <p className="text-xs uppercase tracking-[0.3em] text-slate-400">{eyebrow}</p>
        <h3 className="mt-4 text-sm font-medium text-slate-300">{title}</h3>
        <p className="mt-3 text-3xl font-semibold text-white">{value}</p>
        <p className="mt-3 text-sm text-slate-400">{detail}</p>
      </div>
    </div>
  )
}

function Section({ title, subtitle, children, tall = false }) {
  return (
    <section className={`glass-card p-6 ${tall ? "min-h-[420px]" : ""}`}>
      <div className="mb-6 flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-white">{title}</h2>
          <p className="mt-2 text-sm text-slate-400">{subtitle}</p>
        </div>
      </div>
      {children}
    </section>
  )
}

function StatusPill({ label, active }) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium uppercase tracking-[0.24em] ${
        active
          ? "border-emerald-400/30 bg-emerald-400/15 text-emerald-200"
          : "border-rose-400/30 bg-rose-400/15 text-rose-200"
      }`}
    >
      {label}
    </span>
  )
}

function App() {
  const { data, isLoading, error } = useDashboardData()

  if (isLoading && !data) {
    return (
      <div className="app-shell flex min-h-screen items-center justify-center">
        <div className="glass-card max-w-xl p-10 text-center">
          <p className="text-xs uppercase tracking-[0.32em] text-cyan-300">ChronoCast AI</p>
          <h1 className="mt-4 text-4xl font-semibold text-white">Bootstrapping trading intelligence</h1>
          <p className="mt-4 text-sm text-slate-400">
            Fetching BTC forecasts, MLflow experiments, drift telemetry, and ROI simulations.
          </p>
        </div>
      </div>
    )
  }

  if (error && !data) {
    return (
      <div className="app-shell flex min-h-screen items-center justify-center px-6">
        <div className="glass-card max-w-xl p-10 text-center">
          <p className="text-xs uppercase tracking-[0.32em] text-rose-300">API Error</p>
          <h1 className="mt-4 text-4xl font-semibold text-white">Dashboard data could not be loaded</h1>
          <p className="mt-4 text-sm text-slate-400">{error.message}</p>
        </div>
      </div>
    )
  }

  const predictions = data?.predictions ?? {}
  const experiments = data?.experiments ?? { summary: {}, runs: [] }
  const monitoring = data?.monitoring ?? { features: [], drifted_features: [] }
  const models = data?.models ?? { leaderboard: [], versions: [] }
  const roi = data?.roi ?? { scenarios: [], equity_curve: { strategy: [], buy_and_hold: [] } }
  const abTesting = data?.abTesting ?? { variants: [], history: [] }

  const history = predictions.history ?? []
  const forecastPoints = predictions.forecast_points ?? []
  const predictionLabels = [...history.map((item) => item.date), ...forecastPoints.map((item) => item.date)]
  const priceHistoryData = history.map((item) => item.close)
  const forecastSeries = [
    ...new Array(Math.max(history.length - 1, 0)).fill(null),
    history.length ? history[history.length - 1].close : null,
    ...forecastPoints.map((item) => item.predicted_close),
  ]

  const priceChartData = {
    labels: predictionLabels,
    datasets: [
      {
        label: "BTC Close",
        data: [...priceHistoryData, ...new Array(forecastPoints.length).fill(null)],
        borderColor: "#38bdf8",
        backgroundColor: "rgba(56, 189, 248, 0.16)",
        fill: true,
        pointRadius: 0,
        borderWidth: 2,
        tension: 0.34,
      },
      {
        label: "Forecast Trajectory",
        data: forecastSeries,
        borderColor: "#34d399",
        backgroundColor: "rgba(52, 211, 153, 0.12)",
        borderDash: [6, 6],
        pointRadius: 0,
        borderWidth: 2,
        tension: 0.32,
      },
    ],
  }

  const leaderboard = models.leaderboard ?? []
  const performanceChartData = {
    labels: leaderboard.map((item) => item.model_type.replace("_", " ").toUpperCase()),
    datasets: [
      {
        label: "MAE",
        data: leaderboard.map((item) => item.mae),
        backgroundColor: "rgba(56, 189, 248, 0.72)",
        borderRadius: 14,
      },
      {
        label: "RMSE",
        data: leaderboard.map((item) => item.rmse),
        backgroundColor: "rgba(251, 191, 36, 0.72)",
        borderRadius: 14,
      },
    ],
  }

  const roiChartData = {
    labels: (roi.equity_curve?.strategy ?? []).map((item) => item.date),
    datasets: [
      {
        label: "ChronoCast Strategy",
        data: (roi.equity_curve?.strategy ?? []).map((item) => item.value),
        borderColor: "#34d399",
        backgroundColor: "rgba(52, 211, 153, 0.14)",
        fill: true,
        pointRadius: 0,
        tension: 0.3,
      },
      {
        label: "Buy & Hold",
        data: (roi.equity_curve?.buy_and_hold ?? []).map((item) => item.value),
        borderColor: "#f59e0b",
        backgroundColor: "rgba(245, 158, 11, 0.12)",
        fill: true,
        pointRadius: 0,
        tension: 0.3,
      },
    ],
  }

  const abChartData = {
    labels: (abTesting.history ?? []).map((item) => item.date),
    datasets: [
      {
        label: "Control",
        data: (abTesting.history ?? []).map((item) => item.control_reward),
        borderColor: "#60a5fa",
        backgroundColor: "rgba(96, 165, 250, 0.12)",
        fill: true,
        pointRadius: 0,
        tension: 0.32,
      },
      {
        label: "Challenger",
        data: (abTesting.history ?? []).map((item) => item.challenger_reward),
        borderColor: "#34d399",
        backgroundColor: "rgba(52, 211, 153, 0.12)",
        fill: true,
        pointRadius: 0,
        tension: 0.32,
      },
    ],
  }

  const abDistributionData = {
    labels: (abTesting.variants ?? []).map((item) => item.variant),
    datasets: [
      {
        data: (abTesting.variants ?? []).map((item) => item.traffic_share),
        backgroundColor: ["rgba(96, 165, 250, 0.85)", "rgba(52, 211, 153, 0.85)"],
        borderWidth: 0,
      },
    ],
  }

  const driftRatio = Number(monitoring.share_drifted_features ?? monitoring.drift_score ?? 0)
  const topRuns = (experiments.runs ?? []).slice(0, 5)
  const topDriftFeatures = (monitoring.features ?? []).slice(0, 5)
  const roiScenarios = roi.scenarios ?? []

  return (
    <div className="app-shell min-h-screen px-5 py-6 md:px-8 lg:px-10">
      <div className="mx-auto max-w-[1600px]">
        <header className="glass-card mb-8 overflow-hidden p-8">
          <div className="absolute inset-x-0 top-0 h-32 bg-gradient-to-r from-cyan-500/10 via-transparent to-emerald-400/10" />
          <div className="relative flex flex-col gap-8 xl:flex-row xl:items-end xl:justify-between">
            <div className="max-w-3xl">
              <p className="text-xs uppercase tracking-[0.38em] text-cyan-300">BTC Forecasting ML Platform</p>
              <h1 className="mt-4 max-w-3xl text-4xl font-semibold leading-tight text-white md:text-5xl">
                ChronoCast AI trades the gap between market noise and production-grade forecasting.
              </h1>
              <p className="mt-5 max-w-2xl text-sm leading-7 text-slate-300 md:text-base">
                Live market context, model registry intelligence, drift surveillance, experiment telemetry,
                ROI simulation, and challenger tests in one decision surface.
              </p>
            </div>

            <div className="grid gap-3 text-sm text-slate-300">
              <div className="flex items-center gap-3">
                <StatusPill label={predictions.drift_status || "Unknown"} active={predictions.drift_status === "No Drift"} />
                <span>Refresh cadence: 30s</span>
              </div>
              <div>Production model: {predictions.model_name || "Unavailable"}</div>
              <div>Model version: {predictions.model_version ?? "N/A"}</div>
              <div>Last market update: {predictions.last_updated || "N/A"}</div>
            </div>
          </div>
        </header>

        <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard
            eyebrow="BTC Market Overview"
            title="Latest Spot"
            value={formatCurrency(predictions.latest_price)}
            detail={`${formatNumber(predictions.market?.change_24h_pct, "%")} over the last 24h`}
            tone="cyan"
          />
          <MetricCard
            eyebrow="Next Candle Forecast"
            title="Predicted Close"
            value={formatCurrency(predictions.predicted_price)}
            detail={`${predictions.model_type || "Model"} inference from MLflow production registry`}
            tone="emerald"
          />
          <MetricCard
            eyebrow="Model Performance"
            title="MAE"
            value={formatNumber(predictions.mae)}
            detail={`RMSE ${formatNumber(predictions.rmse)} across the active champion`}
            tone="amber"
          />
          <MetricCard
            eyebrow="Drift Monitoring"
            title="Drift Score"
            value={formatNumber(driftRatio * 100, "%")}
            detail={`${monitoring.drifted_features?.length ?? 0} drifted features in the active window`}
            tone={driftRatio > 0 ? "rose" : "emerald"}
          />
        </section>

        <section className="mt-8 grid gap-5 xl:grid-cols-[1.5fr_1fr]">
          <Section
            title="Prediction Charts"
            subtitle="BTC close history and projected price path from the current production model."
            tall
          >
            <div className="h-[360px]">
              <Line data={priceChartData} options={chartOptions} />
            </div>
          </Section>

          <Section
            title="BTC Market Overview"
            subtitle="Current market regime using the latest feature-engineered snapshot."
            tall
          >
            <div className="grid gap-4">
              <OverviewRow label="7D High" value={formatCurrency(predictions.market?.high_7d)} />
              <OverviewRow label="7D Low" value={formatCurrency(predictions.market?.low_7d)} />
              <OverviewRow label="Avg Volume 7D" value={formatNumber(predictions.market?.avg_volume_7d)} />
              <OverviewRow label="30D Volatility" value={formatNumber(predictions.market?.volatility_30d_pct, "%")} />
              <OverviewRow label="Forecast Spread" value={formatCurrency((predictions.predicted_price ?? 0) - (predictions.latest_price ?? 0))} />
            </div>
            <div className="mt-8 rounded-[24px] border border-white/10 bg-white/5 p-5">
              <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Monitoring Context</p>
              <p className="mt-3 text-sm leading-7 text-slate-300">
                Reference window: {monitoring.reference_window?.start} to {monitoring.reference_window?.end}
              </p>
              <p className="text-sm leading-7 text-slate-300">
                Current window: {monitoring.current_window?.start} to {monitoring.current_window?.end}
              </p>
            </div>
          </Section>
        </section>

        <section className="mt-8 grid gap-5 xl:grid-cols-2">
          <Section
            title="Model Performance"
            subtitle="Champion-vs-challenger error comparison pulled from MLflow metrics."
            tall
          >
            <div className="h-[320px]">
              <Bar data={performanceChartData} options={chartOptions} />
            </div>
          </Section>

          <Section
            title="Drift Monitoring"
            subtitle="Feature-level surveillance for the latest reference and current windows."
            tall
          >
            <div className="rounded-full bg-white/5 p-1">
              <div
                className={`h-3 rounded-full ${driftRatio > 0 ? "bg-rose-400" : "bg-emerald-400"}`}
                style={{ width: `${Math.max(driftRatio * 100, 8)}%` }}
              />
            </div>
            <div className="mt-6 grid gap-3">
              {topDriftFeatures.map((item) => (
                <div key={item.feature} className="flex items-center justify-between rounded-2xl border border-white/8 bg-white/5 px-4 py-3">
                  <div>
                    <p className="text-sm font-medium text-white">{item.feature}</p>
                    <p className="text-xs text-slate-400">p-value {formatNumber(item.p_value)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-slate-200">{formatNumber(item.mean_shift_pct, "%")}</p>
                    <p className={`text-xs ${item.drift_detected ? "text-rose-300" : "text-emerald-300"}`}>
                      {item.drift_detected ? "Drift" : "Stable"}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </Section>
        </section>

        <section className="mt-8 grid gap-5 xl:grid-cols-[1.15fr_0.85fr]">
          <Section
            title="MLflow Experiments"
            subtitle="Recent experiment runs, metrics, and execution status."
            tall
          >
            <div className="overflow-hidden rounded-[24px] border border-white/10 bg-slate-950/35">
              <div className="grid grid-cols-[1.2fr_0.8fr_0.7fr_0.7fr_0.8fr] gap-4 border-b border-white/10 px-5 py-4 text-xs uppercase tracking-[0.24em] text-slate-400">
                <span>Run</span>
                <span>Model</span>
                <span>MAE</span>
                <span>RMSE</span>
                <span>Status</span>
              </div>
              {topRuns.map((run) => (
                <div
                  key={run.run_id}
                  className="grid grid-cols-[1.2fr_0.8fr_0.7fr_0.7fr_0.8fr] gap-4 border-b border-white/5 px-5 py-4 text-sm text-slate-300 last:border-b-0"
                >
                  <span>{run.run_name}</span>
                  <span>{run.model_type}</span>
                  <span>{formatNumber(run.metrics?.mae)}</span>
                  <span>{formatNumber(run.metrics?.rmse)}</span>
                  <span>{run.status}</span>
                </div>
              ))}
            </div>
            <div className="mt-5 grid gap-3 md:grid-cols-3">
              <CompactStat label="Total Runs" value={experiments.summary?.total_runs ?? 0} />
              <CompactStat label="Best Run" value={experiments.summary?.best_run_name ?? "N/A"} />
              <CompactStat label="Best MAE" value={formatNumber(experiments.summary?.best_mae)} />
            </div>
          </Section>

          <Section
            title="Model Leaderboard"
            subtitle="Best registered version for each model family."
            tall
          >
            <div className="grid gap-4">
              {leaderboard.map((item, index) => (
                <div key={`${item.model_name}-${item.version}`} className="rounded-[24px] border border-white/8 bg-white/5 p-5">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="text-xs uppercase tracking-[0.28em] text-slate-400">Rank {index + 1}</p>
                      <h3 className="mt-3 text-lg font-semibold text-white">{item.model_name}</h3>
                    </div>
                    <StatusPill label={item.stage} active={item.stage === "Production"} />
                  </div>
                  <div className="mt-5 grid grid-cols-3 gap-3 text-sm">
                    <CompactStat label="Version" value={item.version} />
                    <CompactStat label="MAE" value={formatNumber(item.mae)} />
                    <CompactStat label="RMSE" value={formatNumber(item.rmse)} />
                  </div>
                </div>
              ))}
            </div>
          </Section>
        </section>

        <section className="mt-8 grid gap-5 xl:grid-cols-2">
          <Section
            title="A/B Testing Results"
            subtitle="Offline challenger evaluation derived from recent model leaderboard metrics."
            tall
          >
            <div className="grid gap-5 lg:grid-cols-[0.85fr_1.15fr]">
              <div className="flex flex-col items-center justify-center rounded-[24px] border border-white/10 bg-white/5 p-5">
                <div className="h-[220px] w-[220px]">
                  <Doughnut
                    data={abDistributionData}
                    options={{
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          labels: {
                            color: "#d6e5ff",
                          },
                        },
                      },
                    }}
                  />
                </div>
                <p className="mt-4 text-sm text-slate-400">Traffic split and challenger evaluation coverage.</p>
              </div>
              <div>
                <div className="grid gap-3 md:grid-cols-3">
                  <CompactStat label="Winner" value={abTesting.winner ?? "N/A"} />
                  <CompactStat label="Confidence" value={formatNumber(abTesting.confidence, "%")} />
                  <CompactStat label="Lift" value={formatNumber(abTesting.lift_pct, "%")} />
                </div>
                <div className="mt-5 h-[220px]">
                  <Line data={abChartData} options={chartOptions} />
                </div>
              </div>
            </div>
          </Section>

          <Section
            title="ROI Simulation"
            subtitle="Projected strategy performance versus passive BTC exposure."
            tall
          >
            <div className="grid gap-3 md:grid-cols-3">
              {roiScenarios.map((scenario) => (
                <div key={scenario.label} className="rounded-[24px] border border-white/10 bg-white/5 p-4">
                  <p className="text-xs uppercase tracking-[0.28em] text-slate-400">{scenario.label}</p>
                  <p className="mt-3 text-2xl font-semibold text-white">{formatCurrency(scenario.expected_price)}</p>
                  <p className="mt-2 text-sm text-slate-300">{formatNumber(scenario.roi_pct, "%")} ROI</p>
                  <p className="text-sm text-slate-400">{formatCurrency(scenario.pnl)} PnL</p>
                </div>
              ))}
            </div>
            <div className="mt-6 h-[240px]">
              <Line data={roiChartData} options={chartOptions} />
            </div>
          </Section>
        </section>
      </div>
    </div>
  )
}

function OverviewRow({ label, value }) {
  return (
    <div className="flex items-center justify-between rounded-[22px] border border-white/8 bg-white/5 px-4 py-4">
      <span className="text-sm text-slate-400">{label}</span>
      <span className="text-base font-medium text-white">{value}</span>
    </div>
  )
}

function CompactStat({ label, value }) {
  return (
    <div className="rounded-[22px] border border-white/10 bg-white/5 px-4 py-4">
      <p className="text-xs uppercase tracking-[0.26em] text-slate-400">{label}</p>
      <p className="mt-3 text-base font-medium text-white">{value}</p>
    </div>
  )
}

export default App
