import { startTransition, useEffect, useState } from "react"

import { fetchDashboardData } from "../api"

const DEFAULT_REFRESH_MS = 30000

export function useDashboardData(refreshMs = DEFAULT_REFRESH_MS) {
  const [data, setData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let isMounted = true

    const load = async () => {
      try {
        const nextData = await fetchDashboardData()
        if (!isMounted) {
          return
        }
        startTransition(() => {
          setData(nextData)
          setError(null)
          setIsLoading(false)
        })
      } catch (loadError) {
        if (!isMounted) {
          return
        }
        setError(loadError)
        setIsLoading(false)
      }
    }

    load()
    const intervalId = window.setInterval(load, refreshMs)

    return () => {
      isMounted = false
      window.clearInterval(intervalId)
    }
  }, [refreshMs])

  return {
    data,
    isLoading,
    error,
  }
}
