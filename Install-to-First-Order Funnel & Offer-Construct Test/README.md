# Growth Funnel & First-Order Offer Test Design

**Target company:** FirstClub (growth role)  
**Tools:** DuckDB SQL · Python · pandas · statsmodels · Metabase-ready outputs  
**Benchmark data:** REES46 multi-category e-commerce behavior, October–November 2019 (the two uploaded files are reduced slices, not the full public monthly archives)

> **Important:** This is a public-data portfolio project, not an analysis of FirstClub's internal customer records. The observed funnel is measured from REES46; the offer outcomes are hypothetical and are not presented as experimental results.

## Business question

Where does a shopper journey lose the most sessions, and how should a grocery app test first-order incentives without spending more on discounts than the extra orders are worth?

FirstClub presents itself as a quality-first grocery platform, so this project compares three different incentive constructs rather than assuming that the largest discount is automatically best: free delivery, ₹100 off, and 10% off. The REES46 files provide a large event-log benchmark for funnel mechanics. They do not contain FirstClub data, installs, offer exposure, treatment assignment, customer first-order eligibility, or contribution margin.

## Headline results

| Metric | Result | Interpretation |
|---|---:|---|
| Raw event rows | **8,738,120** | 4,102,283 October + 4,635,837 November events |
| Unique sessions | **1,814,075** | Session-level denominator; sessions without IDs are excluded |
| Unique users | **712,983** | User IDs observed across the two files |
| Sessions with a view | 1,707,990 | At least one view event in the session |
| Sessions with both a view and a cart | 358,190 | Presence-based; does not require event order |
| Sessions with view, cart, and purchase | 45,360 | Presence-based three-event segment |
| Sessions containing a cart | 440,270 | Denominator for overall cart-session purchase rate |
| Cart sessions also containing purchase | 53,519 | Same-session purchase proxy |
| Cart-session purchase rate | **12.16%** | 53,519 / 440,270 |
| Cart-session non-conversion | **87.84%** | 1 minus the rate above |
| Full view → cart → purchase order | 29,973 sessions | Strict first-event-time ordering check |

The uploaded files contain **4.10M October rows and 4.64M November rows**. The public full-month archives are substantially larger (around 42.4M October rows and 67M November rows), and the selection method for the uploaded slices is unknown. All metrics below describe these exact uploaded files and should not be treated as population estimates. The uploaded records do **not** support the original claim of an approximately 70% cart-to-purchase drop-off under this session-level definition. They show an approximately **88% non-conversion rate**. The difference matters: this project uses the observed result, not the previous resume wording.

The session funnel is *presence-based* by default: a session counts at a stage if the event type occurs anywhere in that session. Separate `first_view`, `first_cart`, and `first_purchase` timestamps are also calculated to sanity-check strict event order. Presence-based counts should not be interpreted as unique orders; multiple purchase rows may represent several purchased items in one order.

![Session funnel](charts/session_funnel.png)

Monthly cart-session purchase rate increased from **10.70% in October** to **13.72% in November**. This is descriptive movement in a different retailer's historical event logs, not evidence that an offer caused the change.

![Monthly cart conversion](charts/monthly_cart_conversion.png)

## Three-offer economics

The public FirstClub context used for the scenario is a reported **roughly ₹1,200 average order value**. Recent public reporting in September 2026 also described free delivery as conditional on a ₹299+ basket. These are external business-context references, not figures derived from REES46; see the sources section. The free-delivery test must be defined against FirstClub’s actual in-app fee threshold so the treatment is genuinely different from the current experience. The following are editable assumptions, not known FirstClub unit economics:

- AOV: ₹1,200
- Pre-promo contribution margin: 25% → ₹300 contribution per order
- Free-delivery cost: ₹60 per redemption (assumption)
- ₹100-off cost: ₹100 per redemption
- 10%-off cost: ₹120 on an assumed ₹1,200 basket

| Offer construct | Modeled promo cost per redeemed order | Contribution after offer | Illustrative break-even CAC ceiling* | Approx. conversion lift needed to offset the offer cost** |
|---|---:|---:|---:|---:|
| Free delivery | ₹60 | ₹240 | ₹240 | +3.04 percentage points (+25% relative) |
| ₹100 off | ₹100 | ₹200 | ₹200 | +6.08 percentage points (+50% relative) |
| 10% off | ₹120 | ₹180 | ₹180 | +8.10 percentage points (+66.7% relative) |

![Offer economics scenario](charts/offer_economics_scenario.png)

\* The CAC ceiling is a simple scenario ceiling equal to contribution after the modeled offer cost. It excludes any costs not already reflected in the assumed contribution margin, including other fulfillment, wastage, refunds, and acquisition costs. Finance must replace these assumptions before a business decision.

\** This compares the observed REES46 cart-session purchase-rate proxy with the treatment rate needed for order contribution per eligible shopper not to fall: `p_treatment × (contribution − offer cost) ≥ p_baseline × contribution`. It is a scenario calculation, not a measured offer response.

The model does not declare a winner. Free delivery is cheaper under the current assumptions, while cash-off offers create a larger contribution hurdle. For a quality-led grocery proposition, free delivery is a sensible *hypothesis to test first*, not a validated winner.

## Proposed controlled experiment

**Target cohort:** customers verified as first-order eligible, randomized at their first cart event. The source dataset cannot identify this cohort; FirstClub order history must supply that eligibility check.

**Arms:** holdout with no offer; free delivery; ₹100 off; 10% off. Randomize persistently at user/account level and prevent cross-arm exposure. Apply consistent delivery-area, minimum-basket, and product eligibility rules to every arm except the treatment itself.

**Primary metric:** paid first order within 24 hours of first-cart offer exposure among first-order-eligible users.  
**Guardrails:** contribution per eligible user, gross contribution per order, basket value, cancellation/refund rate, fulfillment failure, offer redemption, and 30-day repeat purchase.

The preliminary sample-size plan uses a 12.16% historical session-level cart-to-purchase proxy, a 3-percentage-point absolute minimum detectable lift, 80% power, and a Bonferroni-adjusted per-comparison alpha of 0.05 / 3 = 0.0167 for three offer-vs-control tests. This gives approximately **2,736 eligible users per arm** (10,944 across four arms). With a 10% practical buffer, plan for roughly **3,010 per arm / 12,040 total**.

This is a planning estimate only. Before launching, recompute the sample size using FirstClub's measured conversion among the actual first-order-eligible cart cohort; the REES46 session proxy is not a substitute for that baseline.

## Reproduce the project

The raw `.csv.gz` files are not bundled in this archive because they are large. Keep your original source files and place them at:

```text
data/raw/2019-Oct.csv.gz
data/raw/2019-Nov.csv.gz
```

Install dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
python src/run_project.py --data-dir data/raw --engine auto
```

`--engine auto` uses native DuckDB when the `duckdb` package is installed; otherwise, it uses a bounded-memory streaming fallback. The bundled result snapshots were generated through the streaming fallback in the authoring environment; DuckDB was not installed there, so the included DuckDB execution path and SQL pack are provided for reproduction but were not run in that environment. To select explicitly:

```bash
python src/run_project.py --data-dir data/raw --engine duckdb
# or
python src/run_project.py --data-dir data/raw --engine stream
```

Outputs are written to `outputs/` and charts to `charts/`. The DuckDB query pack in `sql/` can also be run statement-by-statement in a DuckDB session from the repository root; `01_event_profile.sql` creates `events`, then `02_session_funnel.sql` creates `sessions` and queries the funnel.

## Dashboard

Use `dashboard/metabase_build_guide.md` to build a Metabase dashboard from the dashboard-ready CSVs, or run the DuckDB SQL pack in a self-hosted Metabase setup with its community DuckDB driver. The dashboard should clearly label REES46 as a public benchmark and label offer economics as a scenario.

## Validation status

The bundled outputs were reconciled against raw row counts and cross-checked by automated tests (`python -m pytest -q`; 4 tests passing). Python source files compile. The streaming path generated the supplied result snapshots. The native DuckDB runner is included but still needs a local execution after installing dependencies; it has not been represented as an executed query run here.

## Repository contents

- `src/run_project.py` — orchestration entry point
- `src/analyze_duckdb.py` — native DuckDB implementation
- `src/analyze.py` — chunked streaming session aggregator / fallback
- `src/profile_file.py`, `src/build_outputs.py` — bounded-memory profiling and output preparation for fallback mode
- `src/make_charts.py` — report charts
- `sql/` — reusable DuckDB event QA, session funnel, and offer-economics queries
- `outputs/` — completed analysis CSVs, JSON summary, and supporting monthly profiles
- `dashboard/` — Metabase dashboard build guide
- `docs/` — experiment design, written analysis, source and methodology notes
- `notebooks/` — analysis walkthrough using the completed output tables

## Data and interpretation limitations

1. **Not FirstClub data.** REES46 is an external, historical multi-category retailer dataset from 2019; use it to demonstrate a method, not estimate FirstClub's live conversion.
2. **No install/first-order flags.** Install-to-first-order cannot be measured. First-order eligibility needs internal order history.
3. **No actual offer assignment.** Offer lift, winner, and causal effect are not measurable from these files; only a test design and cost scenarios are provided.
4. **Margin is assumed.** A 25% contribution margin and ₹60 delivery subsidy are placeholders requiring Finance approval.
5. **Event quality.** Some rows have missing session IDs, category/brand fields have substantial missingness, and some price values are non-positive. The price values are not used as INR inputs to the offer model.
6. **Presence versus sequence.** Funnel presence counts can include events in an order other than view → cart → purchase. The strict timestamp check is provided separately.

## References

See [`docs/references.md`](docs/references.md) for source attribution, FirstClub context, and open-source methodology references.
