from grafanalib.core import *
import os

services = [
    "alpr",
    "auth",
    "bot",
    "edrmvs",
    "frontend",
    "koatuu",
    "operations",
    "stats",
    "vin-decoder",
    "wanted"
]

rows = []

for service in services:
    row = Row(
        title=service,
        panels=[
            Graph(
                title="2XX",
                transparent=True,
                dataSource="Prometheus",
                targets=[
                    Target(
                        expr=f"upstream_rq_2xx{{service=\"{service}\"}} - upstream_rq_2xx{{service=\"{service}\"}} offset $__interval",
                        legendFormat="{{hostname}}"
                    )
                ]
            ),
            Graph(
                title="4XX",
                transparent=True,
                dataSource="Prometheus",
                targets=[
                    Target(
                        expr=f"upstream_rq_4xx{{service=\"{service}\"}} - upstream_rq_4xx{{service=\"{service}\"}} offset $__interval",
                        legendFormat="{{hostname}}"
                    )
                ]
            ),
            Graph(
                title="5XX",
                transparent=True,
                dataSource="Prometheus",
                targets=[
                    Target(
                        expr=f"upstream_rq_5xx{{service=\"{service}\"}} - upstream_rq_5xx{{service=\"{service}\"}} offset $__interval",
                        legendFormat="{{hostname}}"
                    )
                ]
            ),
            Graph(
                title="Health",
                transparent=True,
                dataSource="Prometheus",
                targets=[
                    Target(
                        expr=f"membership_healthy{{service=\"{service}\"}}",
                        legendFormat="{{hostname}}"
                    )
                ]
            ),
        ]
    )
    rows.append(row)

rows.insert(0,
    Row(
        title="General",
        panels=[
            Graph(
                title="Total RPM",
                transparent=True,
                dataSource="Prometheus",
                targets=[
                    Target(
                        expr="sum(rate(upstream_rq_total[1m])) by (service)",
                        legendFormat="{{hostname}}"
                    )
                ]
            ),
        ]
    )
)

dashboard = Dashboard(
    title="Services Dashboard",
    rows=rows
).auto_panel_ids()
