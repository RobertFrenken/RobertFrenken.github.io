#!/usr/bin/env python3
from __future__ import annotations

import html as html_lib
import json
from pathlib import Path

import altair as alt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_static" / "oil_price_tracker_widget.html"


def main() -> int:
    alt.data_transformers.disable_max_rows()

    benchmarks = {
        "WTI monthly (spliced)": {
            "series_id": "WTISPLC",
            "price_label": "Spliced WTI spot price",
        },
        "Brent daily": {
            "series_id": "DCOILBRENTEU",
            "price_label": "Brent crude spot price",
        },
        "WTI daily": {
            "series_id": "DCOILWTICO",
            "price_label": "WTI Cushing crude spot price",
        },
    }

    benchmark = "WTI monthly (spliced)"
    series_id = benchmarks[benchmark]["series_id"]
    price_label = benchmarks[benchmark]["price_label"]

    prices = pd.read_csv(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}")
    prices = prices.rename(columns={"observation_date": "date", series_id: "price_usd_per_barrel"})
    prices["date"] = pd.to_datetime(prices["date"])
    prices["price_usd_per_barrel"] = pd.to_numeric(prices["price_usd_per_barrel"], errors="coerce")
    prices = prices.dropna(subset=["price_usd_per_barrel"]).sort_values("date")

    events = pd.read_csv(ROOT / "posts" / "oil_price_tracker_events.csv", parse_dates=["date"])
    events["tags"] = events["tags"].fillna("")

    prices_for_join = (
        prices[["date", "price_usd_per_barrel"]]
        .rename(columns={"date": "price_date"})
        .sort_values("price_date")
    )
    events_for_join = events.rename(columns={"date": "event_date"}).sort_values("event_date")

    previous_price = pd.merge_asof(
        events_for_join,
        prices_for_join,
        left_on="event_date",
        right_on="price_date",
        direction="backward",
    )
    next_price = pd.merge_asof(
        events_for_join,
        prices_for_join,
        left_on="event_date",
        right_on="price_date",
        direction="forward",
    )

    previous_gap = (events_for_join["event_date"] - previous_price["price_date"]).abs()
    next_gap = (next_price["price_date"] - events_for_join["event_date"]).abs()

    use_next = next_price["price_date"].notna() & (
        previous_price["price_date"].isna() | (next_gap < previous_gap)
    )

    events_joined = previous_price.copy()
    events_joined.loc[use_next, ["price_date", "price_usd_per_barrel"]] = next_price.loc[
        use_next, ["price_date", "price_usd_per_barrel"]
    ].to_numpy()
    events_joined["days_from_price_date"] = (
        events_joined["event_date"] - events_joined["price_date"]
    ).dt.days.abs()
    events_joined["days_from_price_date"] = events_joined["days_from_price_date"].astype("Int64")
    events_joined["event"] = True
    events_joined["date"] = events_joined["price_date"]
    events_joined = events_joined.drop(columns=["price_date"])

    start_date = "1974-01-01"
    prices_recent = prices[prices["date"] >= start_date].copy()
    events_recent = events_joined[events_joined["date"] >= start_date].copy()
    min_year = int(prices["date"].dt.year.min())
    max_year = int(prices["date"].dt.year.max())
    tag_options = sorted(
        {
            tag.strip()
            for value in events["tags"].fillna("")
            for tag in str(value).split(";")
            if tag.strip()
        }
    )

    brush = alt.selection_interval(
        encodings=["x"],
        clear="dblclick",
    )

    tooltip_fields = [
        alt.Tooltip("event_date:T", title="Event date", format="%Y-%m-%d", formatType="utc"),
        alt.Tooltip("date:T", title="Matched price date", format="%Y-%m-%d", formatType="utc"),
        alt.Tooltip("price_usd_per_barrel:Q", title="Price", format="$.2f"),
        alt.Tooltip("countries:N", title="Country/countries"),
        alt.Tooltip("tags:N", title="Tags"),
        alt.Tooltip("description:N", title="Event"),
    ]

    overview = alt.layer(
        alt.Chart(prices).mark_line(color="#1f4e79").encode(
            x=alt.X(
                "date:T",
                title="Date",
                scale=alt.Scale(type="utc"),
                axis=alt.Axis(format="%Y", formatType="utc"),
            ),
            y=alt.Y("price_usd_per_barrel:Q", title="USD per barrel"),
            tooltip=[
                alt.Tooltip("date:T", title="Date", format="%Y-%m-%d", formatType="utc"),
                alt.Tooltip("price_usd_per_barrel:Q", title="Price", format="$.2f"),
            ],
        ),
        alt.Chart(events_joined).mark_point(
            filled=True,
            size=55,
            color="#c1121f",
            stroke="white",
            strokeWidth=0.75,
        ).encode(
            x=alt.X("date:T", scale=alt.Scale(type="utc")),
            y="price_usd_per_barrel:Q",
            tooltip=tooltip_fields,
        ),
    ).properties(
        title=f"{price_label} with market-moving events",
        width=700,
        height=260,
    ).add_params(brush)

    detail = alt.layer(
        alt.Chart(prices_recent).mark_line(color="#1f4e79").encode(
            x=alt.X(
                "date:T",
                title="Date",
                scale=alt.Scale(type="utc", domain=brush),
                axis=alt.Axis(format="%Y-%m", formatType="utc"),
            ),
            y=alt.Y("price_usd_per_barrel:Q", title="USD per barrel"),
            tooltip=[
                alt.Tooltip("date:T", title="Date", format="%Y-%m-%d", formatType="utc"),
                alt.Tooltip("price_usd_per_barrel:Q", title="Price", format="$.2f"),
            ],
        ),
        alt.Chart(events_recent).mark_point(
            filled=True,
            size=85,
            color="#c1121f",
            stroke="white",
            strokeWidth=0.75,
        ).encode(
            x=alt.X("date:T", scale=alt.Scale(type="utc")),
            y="price_usd_per_barrel:Q",
            opacity=alt.value(0.9),
            tooltip=tooltip_fields,
        ),
    ).properties(
        title="Drag a brush in the top panel to zoom the detail view",
        width=700,
        height=320,
    )

    chart = (
        alt.vconcat(overview, detail)
        .resolve_scale(y="shared")
        .configure_axis(grid=True)
        .configure_view(strokeWidth=0)
    )
    base_spec = chart.to_dict()
    base_spec_json = json.dumps(base_spec, ensure_ascii=False).replace("</", "<\\/")
    config_json = json.dumps(
        {
            "defaultWindow": "recent",
            "tagOptions": tag_options,
            "minYear": min_year,
            "maxYear": max_year,
            "defaultStartYear": 1974,
            "defaultEndYear": max_year,
        },
        ensure_ascii=False,
    )

    html = f"""
<div class="oil-tracker-shell" data-oil-tracker-shell>
  <div class="oil-tracker-controls">
    <label class="oil-tracker-field">
      Time window
      <select class="oil-tracker-select" data-oil-window>
        <option value="recent">Mid-1970s onward</option>
        <option value="full">Full history</option>
        <option value="iran80s">1980s Gulf conflicts</option>
        <option value="midEast2020s">2020s Middle East conflicts</option>
      </select>
    </label>
    <div class="oil-tracker-range-group">
      <label class="oil-tracker-field oil-tracker-range-field">
        Start year <span data-oil-start-label></span>
        <input class="oil-tracker-range" type="range" min="{min_year}" max="{max_year}" step="1" data-oil-start-year>
      </label>
      <label class="oil-tracker-field oil-tracker-range-field">
        End year <span data-oil-end-label></span>
        <input class="oil-tracker-range" type="range" min="{min_year}" max="{max_year}" step="1" data-oil-end-year>
      </label>
    </div>
    <label class="oil-tracker-field">
      Tags
      <select class="oil-tracker-select oil-tracker-tag-select" data-oil-tags multiple size="6">
        {"".join(f'<option value="{html_lib.escape(tag, quote=True)}">{html_lib.escape(tag, quote=True)}</option>' for tag in tag_options)}
      </select>
    </label>
    <button class="oil-tracker-btn" type="button" data-oil-clear>Clear tags</button>
    <div class="oil-tracker-status" data-oil-status></div>
  </div>
  <div class="oil-tracker-chart" data-oil-chart></div>
  <div class="oil-tracker-backdrop" data-oil-backdrop></div>
  <div class="oil-tracker-popup" role="dialog" aria-modal="true" aria-live="polite" aria-label="Oil market event details" data-oil-popup>
    <button class="oil-tracker-popup-close" aria-label="Close event popup" data-oil-close>&times;</button>
    <div class="oil-tracker-popup-content" data-oil-popup-content></div>
  </div>
  <script id="oil-tracker-spec" type="application/json">{base_spec_json}</script>
  <script id="oil-tracker-config" type="application/json">{config_json}</script>
</div>
<script src="./vendor/vega.min.js"></script>
<script src="./vendor/vega-lite.min.js"></script>
<script src="./vendor/vega-embed.min.js"></script>
<script src="./oil_price_tracker.js"></script>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
