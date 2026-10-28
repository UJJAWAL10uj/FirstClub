# Grocery Growth, Analytics & AI Portfolio

A collection of four projects exploring how a quality-first grocery business can improve customer acquisition, retention, inventory availability, and lifecycle marketing through data analysis, experimentation, forecasting, and automation.

The projects use public datasets or explicitly stated modelling assumptions. Results from historical analysis and simulations are distinguished from outcomes that would require a live experiment.

> **Dashboard note:** Metabase dashboards are referenced as a reporting target in the project stack, but I did not have access to a Metabase instance for these projects. To make the analysis easy to explore and share, I created standalone HTML dashboards where applicable. These HTML dashboards are browser-openable alternatives, not live Metabase deployments.

## Projects at a Glance

| Project | Business Question | Tools | Main Output |
|---|---|---|---|
| [1. Install-to-First-Order Funnel & Offer-Construct Test](#1-install-to-first-order-funnel--offer-construct-test) | Where do prospective customers drop off, and which first-order offer is worth testing? | SQL, DuckDB, Python, statsmodels, HTML dashboards | Funnel diagnostics, offer economics, and experiment sizing |
| [2. Retention Cohorts, Basket Width & Milestone Program](#2-retention-cohorts-basket-width--milestone-program) | Which behaviours are associated with repeat ordering, and could a fifth-order incentive pay off? | SQL, Python, statsmodels, HTML dashboard | Cohort retention, basket-width analysis, and a break-even model |
| [3. StockSense: SKU Demand Forecasting & Reorder Points](#3-stocksense-sku-demand-forecasting--reorder-points) | How can grocery inventory be planned to reduce stockouts without holding excessive stock? | Python, pandas, scikit-learn, SQL, Power BI | Weekly demand forecasts and simulated inventory policies |
| [4. AI-Powered Grocery CRM & Lifecycle Automation](#4-ai-powered-grocery-crm--lifecycle-automation) | How can customer segments receive more relevant campaigns with less manual work? | n8n, Google Sheets, LLM-based logic | Automated segmentation and lifecycle campaign workflow |

---

## 1. Install-to-First-Order Funnel & Offer-Construct Test

**Stack:** SQL · DuckDB · Python · statsmodels · HTML dashboard  
**Dataset:** Public REES46 e-commerce event data

### Objective
Understand where users abandon the shopping journey and design measurable first-order offer tests without assuming that larger discounts automatically produce better growth.

### Approach
- Processed more than **8.7 million event rows** using DuckDB.
- Mapped the shopping journey across product views, cart activity, and purchases.
- Calculated session-level funnel conversion and drop-off rates.
- Compared three proposed first-order offer constructs: **free delivery, ₹100 off, and 10% off**.
- Modelled sample-size requirements and break-even acquisition economics using explicit assumptions.
- Created a standalone HTML dashboard to make key funnel and offer-economics outputs easy to explore without requiring access to a hosted BI instance.

### Key finding
In the analysed data, the view-to-cart rate was approximately **21.0%**, while the same-session cart-to-purchase conversion rate was approximately **12.2%**—an approximately **87.8% drop-off** from cart sessions to purchasing sessions under that definition.

### Business application
Prioritise investigation of cart and checkout friction, then test offer constructs against a control group. Compare incremental first orders and contribution economics, not conversion rate alone.

### Important limitation
The dataset is a public e-commerce event dataset, not FirstClub's internal data. The offer tests are proposed experiments and modelled economics, not evidence that any offer has already improved FirstClub's conversion.

---

## 2. Retention Cohorts, Basket Width & Milestone Program

**Stack:** SQL · Python · statsmodels · HTML dashboard  
**Dataset:** Public Instacart Market Basket Analysis data

### Objective
Explore repeat-order behaviour, assess whether shopping across more departments is associated with retention, and model a milestone incentive for a customer's fifth order.

### Approach
- Analysed approximately **3.4 million orders** from more than **200,000 users**.
- Reconstructed relative order timelines using the dataset's `days_since_prior_order` field.
- Defined basket width as the number of distinct departments purchased across a customer's first three orders, excluding non-informative department categories.
- Built weekly retention views and compared customer cohorts.
- Examined whether the apparent basket-width relationship remained after accounting for basket size and other behavioural differences.
- Modelled a **free-delivery-on-the-fifth-order** program using illustrative fee, margin, and order-frequency assumptions.
- Created a standalone HTML dashboard because a live Metabase instance was not available.

### Key findings
- The raw comparison showed wide-basket customers placing approximately **1.11× as many repeat orders** as the comparison group.
- After adjustment for other behavioural factors, the apparent advantage did not hold; the adjusted association was approximately **0.92×**. This is an association, not proof that basket width reduces retention.
- Approximately **88.4%** of customers who placed a fourth order went on to place a fifth in the observed data.
- Under one illustrative economic scenario, the model estimated a break-even order-frequency lift of approximately **4.6%**. This is a modelled threshold, not a measured experiment result.

### Business application
Treat cross-category discovery and fifth-order free delivery as hypotheses to test. A controlled experiment should measure incremental orders and contribution profit after incentive costs.

### Important limitations
Instacart's public dataset does not provide full calendar dates, and the observed order-gap values are capped at 30 days. The dataset also has selection limitations, and historical associations cannot establish causal impact. The break-even result depends on assumed economics that should be replaced with company-specific values.

---

## 3. StockSense: SKU Demand Forecasting & Reorder Points

**Stack:** Python · pandas · scikit-learn · SQL · Power BI  
**Dataset:** Public Corporación Favorita grocery sales data

### Objective
Forecast weekly demand across **200 grocery SKUs** and translate the forecasts into inventory policies that balance product availability with excess stock.

### Approach
- Prepared historical sales data for SKU-level demand analysis.
- Built weekly demand forecasts and compared model performance with a seasonal-naive baseline.
- Evaluated forecasts using **Weighted Absolute Percentage Error (WAPE)**.
- Used demand and lead-time assumptions to estimate safety stock and reorder points.
- Simulated inventory outcomes to compare stockout and excess-inventory behaviour under alternative policies.
- Designed Power BI reporting to make SKU-level demand and inventory signals easier to review.

### Reported results
- **18% lower WAPE** than the seasonal-naive baseline.
- **35% fewer simulated stockouts**.
- **20% less simulated excess inventory**.

### Business application
Use forecasts and reorder points to help prioritise replenishment, reduce missed sales caused by unavailable products, and avoid unnecessary inventory holding.

### Important limitation
The stockout and excess-inventory improvements are simulation results, not verified outcomes from a live retailer deployment. Real-world performance would depend on forecast drift, supplier lead times, perishability, minimum order quantities, and operational execution.

---

## 4. AI-Powered Grocery CRM & Lifecycle Automation

**Stack:** n8n · Google Sheets · Large Language Models (LLMs)

### Objective
Design an AI-assisted workflow that organises customer information into actionable segments and supports more relevant lifecycle campaigns with less repetitive manual work.

### Approach
- Used **n8n** to orchestrate workflow steps and connect services.
- Used Google Sheets as a lightweight customer and campaign-tracking layer.
- Applied LLM-based logic to support customer segmentation and campaign personalisation.
- Structured campaign use cases around:
  - **First-order conversion:** helping new users move from install or browse to purchase.
  - **Replenishment:** prompting customers when a repeat purchase may be relevant.
  - **Win-back:** re-engaging customers who have become inactive.
- Designed performance tracking around conversion, repeat purchases, and campaign ROI.

### Business application
A workflow like this can help growth teams create more consistent, segment-aware campaigns while retaining human review for message quality, customer appropriateness, and business rules.

### Measurement plan
Evaluate incremental conversion, repeat-purchase rate, revenue or contribution per targeted customer, campaign cost, opt-outs, and complaints. Where possible, compare campaign recipients with a randomised holdout group.

### Important limitation
The workflow description represents an automation design. Business impact should only be claimed after the workflow is deployed and evaluated against a suitable baseline or control group.

---

## Common Principles Across the Projects

- **Start with a business question:** define the decision the analysis should inform before selecting tools.
- **Measure the full funnel:** distinguish activity metrics from outcomes such as completed orders, repeat purchases, and contribution profit.
- **Use experiments where possible:** separate correlation, modelled estimates, simulation results, and causal evidence.
- **Make assumptions explicit:** especially for offer economics, inventory simulations, and break-even calculations.
- **Use AI with validation:** AI can accelerate coding and workflow design, but data definitions, outputs, and customer-facing decisions still require review.
- **Design for execution:** turn analysis into a campaign, inventory policy, dashboard, or experiment that a team can act on.

## Suggested Repository Structure

```text
grocery-growth-analytics-portfolio/
├── README.md
├── project-1-funnel-offer-test/
│   ├── data/              # Keep large/raw datasets out of Git where appropriate
│   ├── src/
│   ├── outputs/
│   └── docs/
├── project-2-retention-milestone/
│   ├── data/
│   ├── src/
│   ├── outputs/
│   └── docs/
├── project-3-stocksense/
│   ├── data/
│   ├── src/
│   ├── models/
│   └── reports/
└── project-4-ai-grocery-crm/
    ├── workflows/
    ├── examples/
    └── docs/
```

The structure above is a suggested organisation; adapt the folder names to match the files actually included in the repository.

## Reproducibility & Data Notes

- Use the original dataset documentation and licences when redistributing or referencing public data.
- Do not commit private customer data, credentials, API keys, or production campaign information.
- Document metric definitions, date windows, exclusions, assumptions, and random seeds where applicable.
- Include setup instructions and exact run commands in each project's own README.
- Label simulated or modelled results clearly and update them if a reproducible rerun produces different numbers.

---

*Portfolio focus: Growth Analytics · Customer Acquisition · Retention · CRM Automation · Demand Forecasting · Experimentation*
