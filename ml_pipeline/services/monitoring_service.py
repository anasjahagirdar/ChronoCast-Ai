from __future__ import annotations

import json
from datetime import datetime, timezone

from scipy.stats import ks_2samp

from ml_pipeline.config import FEATURE_COLUMNS, REPORTS_DIR
from ml_pipeline.services.data_service import load_feature_dataset


DRIFT_SUMMARY_PATH = REPORTS_DIR / "drift_summary.json"
DRIFT_HTML_PATH = REPORTS_DIR / "drift_report.html"


def compute_drift_summary(window: int = 90) -> dict[str, object]:
    frame = load_feature_dataset().copy()
    if len(frame.index) < 20:
        raise ValueError("Not enough feature rows are available for drift analysis.")

    if len(frame.index) < window * 2:
        window = max(len(frame.index) // 2, 10)

    reference = frame.iloc[-(window * 2) : -window]
    current = frame.iloc[-window:]

    feature_summaries = []
    drifted = []

    for feature_name in FEATURE_COLUMNS:
        ref_series = reference[feature_name].astype(float)
        cur_series = current[feature_name].astype(float)
        ref_mean = float(ref_series.mean())
        cur_mean = float(cur_series.mean())
        denominator = abs(ref_mean) if abs(ref_mean) > 1e-9 else 1.0
        mean_shift_pct = float(((cur_mean - ref_mean) / denominator) * 100)
        ks_result = ks_2samp(ref_series, cur_series)
        drift_detected = bool(ks_result.pvalue < 0.05 or abs(mean_shift_pct) > 12.5)

        feature_summary = {
            "feature": feature_name,
            "reference_mean": ref_mean,
            "current_mean": cur_mean,
            "mean_shift_pct": mean_shift_pct,
            "p_value": float(ks_result.pvalue),
            "drift_detected": drift_detected,
        }
        feature_summaries.append(feature_summary)
        if drift_detected:
            drifted.append(feature_name)

    drift_score = round(len(drifted) / len(FEATURE_COLUMNS), 4)
    status = "Drift Detected" if drifted else "No Drift"

    return {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "status": status,
        "drift_score": drift_score,
        "share_drifted_features": drift_score,
        "drifted_features": drifted,
        "report_path": str(DRIFT_HTML_PATH.as_posix()),
        "reference_window": {
            "start": reference.iloc[0]["date"].date().isoformat(),
            "end": reference.iloc[-1]["date"].date().isoformat(),
        },
        "current_window": {
            "start": current.iloc[0]["date"].date().isoformat(),
            "end": current.iloc[-1]["date"].date().isoformat(),
        },
        "features": feature_summaries,
    }


def _render_html_report(summary: dict[str, object]) -> str:
    rows = []
    for feature in summary["features"]:
        rows.append(
            "<tr>"
            f"<td>{feature['feature']}</td>"
            f"<td>{feature['reference_mean']:.4f}</td>"
            f"<td>{feature['current_mean']:.4f}</td>"
            f"<td>{feature['mean_shift_pct']:.2f}%</td>"
            f"<td>{feature['p_value']:.4f}</td>"
            f"<td>{'Yes' if feature['drift_detected'] else 'No'}</td>"
            "</tr>"
        )

    badge_color = "#fb7185" if summary["status"] == "Drift Detected" else "#34d399"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ChronoCast Drift Report</title>
  <style>
    body {{ background: #07111f; color: #e5eefb; font-family: Arial, sans-serif; margin: 0; padding: 32px; }}
    .card {{ background: rgba(15, 23, 42, 0.88); border: 1px solid rgba(148, 163, 184, 0.18); border-radius: 20px; padding: 24px; }}
    .status {{ display: inline-block; padding: 8px 12px; border-radius: 999px; background: {badge_color}; color: #04111f; font-weight: bold; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    th, td {{ padding: 12px; border-bottom: 1px solid rgba(148, 163, 184, 0.14); text-align: left; }}
    th {{ color: #93c5fd; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>ChronoCast AI Drift Monitoring</h1>
    <p class="status">{summary['status']}</p>
    <p>Generated at: {summary['generated_at']}</p>
    <p>Reference window: {summary['reference_window']['start']} to {summary['reference_window']['end']}</p>
    <p>Current window: {summary['current_window']['start']} to {summary['current_window']['end']}</p>
    <p>Drift score: {summary['drift_score']:.2%}</p>
    <table>
      <thead>
        <tr>
          <th>Feature</th>
          <th>Reference Mean</th>
          <th>Current Mean</th>
          <th>Mean Shift</th>
          <th>KS p-value</th>
          <th>Drift</th>
        </tr>
      </thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
  </div>
</body>
</html>"""


def persist_drift_summary(summary: dict[str, object]) -> dict[str, object]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DRIFT_SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    DRIFT_HTML_PATH.write_text(_render_html_report(summary), encoding="utf-8")
    return summary


def get_drift_summary(refresh: bool = False) -> dict[str, object]:
    if refresh or not DRIFT_SUMMARY_PATH.exists():
        return persist_drift_summary(compute_drift_summary())

    return json.loads(DRIFT_SUMMARY_PATH.read_text(encoding="utf-8"))
