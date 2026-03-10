import axios from "axios"

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"
const baseURL = rawBaseUrl.endsWith("/") ? rawBaseUrl.slice(0, -1) : rawBaseUrl

export const api = axios.create({
  baseURL,
  timeout: 15000,
})

export async function fetchDashboardData() {
  const [
    predictions,
    experiments,
    monitoring,
    models,
    roi,
    abTesting,
  ] = await Promise.all([
    api.get("/api/predictions/"),
    api.get("/api/experiments/"),
    api.get("/api/monitoring/drift/"),
    api.get("/api/models/"),
    api.get("/api/roi/"),
    api.get("/api/ab-testing/"),
  ])

  return {
    predictions: predictions.data,
    experiments: experiments.data,
    monitoring: monitoring.data,
    models: models.data,
    roi: roi.data,
    abTesting: abTesting.data,
  }
}
