import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import altair as alt
    import duckdb
    import marimo as mo

    DATABASE_URL = "https://glean-dictionary-duckdb.netlify.app/data/glean_dictionary.duckdb"
    glean_connection = duckdb.connect(":memory:")
    glean_connection.execute(f"ATTACH '{DATABASE_URL}' AS glean_dictionary")

    pass
    return alt, glean_connection, mo


@app.cell
def _(glean_connection, mo):
    _app_names = [
        _row[0]
        for _row in glean_connection.sql(
            "SELECT DISTINCT app_name FROM glean_dictionary.metrics ORDER BY app_name"
        ).fetchall()
    ]

    app_selector = mo.ui.dropdown(
        options=_app_names,
        value="firefox_desktop",
        allow_select_none=False,
        searchable=True,
        label="Application",
        full_width=True,
    )
    app_selector
    return (app_selector,)


@app.cell
def _(app_selector, glean_connection, mo):
    metrics_by_month = mo.sql(
        f"""
        WITH raw_intervals AS (
            SELECT
                name,
                CAST(date_first_seen AS TIMESTAMP) AS started_at,

                CASE
                    WHEN NOT in_source THEN
                        TRY_CAST(
                            JSON_EXTRACT_STRING(dates, '$.last')
                            AS TIMESTAMP
                        )
                END AS removed_at,

                TRY_CAST(
                    TRIM(BOTH '"' FROM CAST(expires AS VARCHAR))
                    AS TIMESTAMP
                ) AS expired_at

            FROM glean_dictionary.metrics
            WHERE app_name = '{app_selector.value}'
        ),

        metric_intervals AS (
            SELECT
                name,
                started_at,
                CASE
                    WHEN removed_at IS NULL THEN expired_at
                    WHEN expired_at IS NULL THEN removed_at
                    ELSE LEAST(removed_at, expired_at)
                END AS ended_at
            FROM raw_intervals
        ),

        bounds AS (
            SELECT DATE_TRUNC('month', MIN(started_at)) AS first_month
            FROM metric_intervals
        ),

        months AS (
            SELECT month
            FROM GENERATE_SERIES(
                (SELECT first_month FROM bounds),
                DATE_TRUNC('month', CURRENT_DATE),
                INTERVAL '1 month'
            ) AS generated(month)
        ),

        snapshots AS (
            SELECT
                month,
                LEAST(
                    CAST(month + INTERVAL '1 month' - INTERVAL '1 day' AS DATE),
                    CURRENT_DATE
                ) AS as_of
            FROM months
        )

        SELECT
            snapshots.month,
            snapshots.as_of,
            COUNT(metric_intervals.name) AS active_metrics
        FROM snapshots
        LEFT JOIN metric_intervals
            ON metric_intervals.started_at
                   < snapshots.as_of + INTERVAL '1 day'
           AND (
               metric_intervals.ended_at IS NULL
               OR metric_intervals.ended_at
                      >= snapshots.as_of + INTERVAL '1 day'
           )
        GROUP BY snapshots.month, snapshots.as_of
        ORDER BY snapshots.month
        """,
        output=False,
        engine=glean_connection
    )
    return (metrics_by_month,)


@app.cell
def _(alt, metrics_by_month):
    _chart = (
        alt.Chart(metrics_by_month)
        .mark_bar()
        .encode(
            x=alt.X(field="month", type="temporal", timeUnit="yearmonth"),
            y=alt.Y(field="active_metrics", type="quantitative"),
            tooltip=[
                alt.Tooltip(field="month", timeUnit="yearmonthdate", title="month"),
                alt.Tooltip(field="active_metrics", format=",.0f"),
            ],
        )
        .properties(
            height=290,
            width="container",
            config={"axis": {"grid": False}},
        )
    )
    _chart
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
