-- 1. Market scale and month-over-month growth
WITH monthly AS (
    SELECT month, SUM(registrations) AS volume
    FROM vahan GROUP BY month
), comparison AS (
    SELECT *, LAG(volume) OVER (ORDER BY month) AS prior_volume
    FROM monthly
)
SELECT month, volume, volume - prior_volume AS change_count,
       100.0 * (volume - prior_volume) / NULLIF(prior_volume, 0) AS growth_pct
FROM comparison ORDER BY month;

-- 2. Annual fuel mix (retain original fuel labels)
WITH fuel_totals AS (
    SELECT fuel, SUM(registrations) AS volume FROM vahan GROUP BY fuel
)
SELECT fuel, volume, 100.0 * volume / SUM(volume) OVER () AS share_pct
FROM fuel_totals ORDER BY volume DESC, fuel;

-- 3. Manufacturer volume versus share for Sep-Oct. Eligibility uses prior volume
WITH maker_month AS (
    SELECT month, maker, SUM(registrations) AS volume
    FROM vahan WHERE month IN ('2025-09-01', '2025-10-01')
    GROUP BY month, maker
), shares AS (
    SELECT *, 100.0 * volume / SUM(volume) OVER (PARTITION BY month) AS share_pct
    FROM maker_month
)
SELECT c.maker, p.volume AS prior_volume, c.volume AS current_volume,
       100.0 * (c.volume - p.volume) / NULLIF(p.volume, 0) AS growth_pct,
       c.share_pct - p.share_pct AS share_change_pp
FROM shares c JOIN shares p ON c.maker = p.maker
WHERE c.month = '2025-10-01' AND p.month = '2025-09-01' AND p.volume >= 1000
ORDER BY growth_pct DESC, c.maker;

-- 4. Fuel contributions to the October change (signed counts)
SELECT fuel,
       SUM(CASE WHEN month = '2025-10-01' THEN registrations ELSE -registrations END) AS contribution
FROM vahan WHERE month IN ('2025-09-01', '2025-10-01')
GROUP BY fuel ORDER BY contribution DESC, fuel;
