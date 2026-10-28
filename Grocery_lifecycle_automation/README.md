# AI-Powered Grocery CRM & Lifecycle Automation

**Portfolio project for growth, CRM, lifecycle marketing, and product analytics roles.**

> **Data honesty:** This repository uses synthetic grocery customers, generated orders, and simulated campaign outcomes. It does not contain FirstClub data and does not claim real campaign lift, conversion, retention, or ROI. The n8n workflow creates reviewable campaign drafts only; it does not send messages.

## 1. Business problem

Grocery customers have different lifecycle needs. A new signup needs a clear path to a first order; a one-time buyer may need a useful reason to return; a repeat customer may be due to replenish essentials; and a formerly active customer may need a win-back journey. Sending one offer to everyone can waste discount budget and create unnecessary contact.

**Objective:** build a simple decision system that turns customer and order history into explainable campaign recommendations, drafts segment-aware copy with an LLM, and tracks campaign funnel and economics.

### Growth hypothesis

Using customer lifecycle signals (order count, recency, spend, preferred category, replenishment cadence, consent, and recent contact history) to choose a relevant campaign should make lifecycle communications more useful than a one-size-fits-all blast. This is a hypothesis to test, not a proven result from the synthetic data.

## 2. What is implemented

- Deterministic lifecycle segmentation with an explainable reason for each decision.
- Marketing-consent, invalid-email, and contact-cooldown suppression rules.
- Controlled offer suggestions; discounting is not the default for every segment.
- Reusable email copy templates, with optional OpenAI copy drafting by campaign type.
- An importable n8n workflow that reads a Google Sheet, groups eligible customers, makes one LLM request per campaign type, expands the copy to customer-level drafts, and appends them to a campaign queue sheet.
- Synthetic customer, order, and historic campaign datasets for a reproducible demo.
- Campaign funnel and economic KPIs: delivery, opens, clicks, conversions, 30-day repeat purchase, attributed revenue, campaign cost, estimated gross profit, and estimated ROI.
- Unit tests for critical consent, cooldown, lifecycle, and KPI logic.
- Optional Streamlit dashboard for reviewing the output.

## 3. Architecture

```text
Synthetic or business-approved customer data
                 |
                 v
     Google Sheets: Customers
                 |
                 v
        n8n Manual Trigger
                 |
                 v
 Validate -> Suppress -> Segment -> Explain decision
                 |
                 v
 Group by campaign type (no customer PII sent to the LLM)
                 |
                 v
 OpenAI generates a reusable copy template per campaign type
                 |
                 v
 Personalize with approved fields and fixed offer text
                 |
                 v
 Google Sheets: Campaign_Queue (draft-only; human approval required)

Campaign history -> KPI calculations -> JSON/CSV + optional dashboard
```

The local Python engine and n8n workflow share the same core segmentation principles. The local run works without API credentials. Set `OPENAI_API_KEY` only when you want the local demo to ask an LLM to write campaign copy.

## 4. Lifecycle segmentation rules

The rules are deliberately interpretable; priority order prevents a customer from being sent multiple overlapping recommendations in the same run.

| Priority | Trigger | Segment / campaign | Default treatment |
|---|---|---|---|
| 1 | Missing/invalid email, no marketing consent, or contacted within the last 7 days | Suppressed | Do not queue |
| 2 | No orders | New Signup / Dormant Signup → First Order Activation | Example: 5% off first order, capped at ₹100 |
| 3 | Exactly one order and last order within 14 days | First-Order Customer → Post-Purchase Reorder | Useful add-ons; no discount by default |
| 4 | Exactly one order and older than 14 days | One-Time Buyer → First-to-Second Order | Example: 5% off next order, capped at ₹100 |
| 5 | 2+ orders and last order at least 45 days ago | Dormant Repeat / High-Value Win-Back | Example: 10% off above ₹799, capped at ₹150 |
| 6 | Spend at least ₹6,000 and inactivity at least 21 days (unless the 45-day win-back rule already matched) | High-Value At-Risk → VIP Re-engagement | Personalization before incentive |
| 7 | Last order is near the stated replenishment cadence | Replenishment Due → Replenishment Reminder | Category-relevant replenishment; no discount by default |
| 8 | Recent repeat order | Active Repeat → Cross-Sell & Habit | Relevant complementary products |
| 9 | Other eligible customers | Active Customer Nurture | Relevant category recommendations |

**These are demo thresholds**, not FirstClub policy. In a real setting, validate them using category buying cycles, margins, customer research, holdout tests, and business-approved offer constraints.

## 5. Repository structure

```text
ai-grocery-crm-lifecycle/
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   └── campaign_history_simulated.csv
├── docs/
│   ├── architecture.md
│   └── google_sheets_setup.md
├── n8n/workflows/
│   └── grocery_lifecycle_automation.json
├── outputs/
│   ├── campaign_queue.csv
│   ├── customer_decisions.csv
│   ├── segment_summary.csv
│   ├── kpi_report.json
│   └── run_summary.md
├── scripts/
│   ├── generate_synthetic_data.py
│   └── run_demo.py
├── src/lifecycle_engine.py
├── tests/test_lifecycle_engine.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## 6. Run locally (Windows / PowerShell)

The core demo requires Python 3.10+ and the standard library only.

```powershell
# 1. Open this project folder in Terminal
cd path\to\ai-grocery-crm-lifecycle

# 2. Generate deterministic synthetic data
py -3 scripts\generate_synthetic_data.py

# 3. Run the lifecycle rules and generate outputs
py -3 scripts\run_demo.py --as-of-date 2026-10-27

# 4. Run tests
py -3 -m unittest discover -s tests -v
```

The `--as-of-date` argument makes the demo reproducible. Use today's date for a fresh evaluation of the sample data, for example `py -3 scripts\run_demo.py --as-of-date 2026-10-27`.

### Optional: generate copy with an LLM

The fallback templates work without an API key. To use OpenAI for one copy template per eligible campaign type:

```powershell
$env:OPENAI_API_KEY = "your-key-here"
py -3 scripts\run_demo.py --as-of-date 2026-10-27 --use-llm
```

Do not paste your API key into source files, workflow JSON, screenshots, GitHub, or the campaign sheet. The LLM only drafts copy. The deterministic engine keeps eligibility, offers, consent, and cooldown decisions outside the model.

### Optional: open the dashboard

```powershell
py -3 -m pip install -r requirements.txt
py -3 -m streamlit run dashboard.py
```

## 7. Connect n8n to Google Sheets and an LLM

The workflow JSON is located at `n8n/workflows/grocery_lifecycle_automation.json`.

1. Create a Google spreadsheet with tabs named `Customers` and `Campaign_Queue`.
2. Import `data/customers.csv` into the `Customers` tab (keep the header row). The template contains 1,000 synthetic customer profiles and dates/order summaries.
3. Put the exact queue headers listed in `docs/google_sheets_setup.md` in row 1 of `Campaign_Queue`.
4. In n8n, import the workflow JSON.
5. In both Google Sheets nodes, replace `YOUR_GOOGLE_SHEET_ID` with your spreadsheet ID and select your Google Sheets OAuth2 credential.
6. In the AI HTTP Request node, create/select an **HTTP Header Auth** credential with header name `Authorization` and value `Bearer YOUR_OPENAI_API_KEY`. The workflow JSON contains no API key.
7. Test with a small sample first. The workflow performs one LLM call per campaign type present in the eligible sample, not one call per customer.
8. Review `Campaign_Queue`: every record should have `status = DRAFT_REQUIRES_REVIEW` and `send_approved = NO`. Actual sending is intentionally not configured.

The first run needs working Google Sheets and LLM credentials. If you don't want to configure credentials yet, use the local Python demo and its deterministic fallback templates.

## 8. Metrics and definitions

The demo reports:

- **Open rate** = opened / delivered
- **Click-through rate** = clicked / delivered
- **Click-to-open rate** = clicked / opened
- **Conversion rate** = converted / delivered
- **30-day repeat-purchase rate** = repeat purchases within 30 days / delivered
- **Attributed revenue** = revenue assigned to a campaign in the synthetic event log
- **Estimated gross profit** = attributed revenue × assumed gross margin (28% by default)
- **Estimated ROI** = (estimated gross profit − delivery cost − redeemed offer discount cost) / (delivery cost + redeemed offer discount cost)

The definitions, simulated data note, and gross margin assumption are recorded in `outputs/kpi_report.json`. In production, align the attribution window, campaign cost, margin and incrementality method with the business. A campaign-attributed order is not necessarily an incremental order; randomized holdouts are needed to estimate lift.

## 9. Validation and safeguards

- Missing consent, invalid email, and the contact cooldown are hard suppressions.
- No email, WhatsApp, SMS, or push message is sent by this repository.
- AI writes only reusable copy templates by campaign type; it does not receive customer names, emails, IDs, or individual purchase histories.
- Offer text is determined by business logic and passed as a placeholder; the model is told not to invent or change offers.
- The campaign queue is explicitly a draft requiring human review.
- Tests cover suppression, activation, win-back, draft-only status, and KPI formulas.

## 10. Known limitations and next iterations

- Sample data and campaign outcomes are synthetic; all performance numbers are illustrative.
- Segmentation is rules-based rather than a trained propensity model.
- The n8n workflow is an importable starter; credentials and spreadsheet IDs must be set by the user.
- Re-running n8n can append duplicate drafts for the same customer/date. Before any production use, add an idempotency lookup on `campaign_id`, persistent contact history, and error/retry handling.
- Email delivery, suppression lists, user-level frequency caps, template rendering, localization, and unsubscribe flows need connection to a compliant sending platform before production.
- A/B tests and holdout groups should be used to compare subject lines, offers, send timing, and segment rules.

## 11. Interview walkthrough

**30-second summary:** “I built a grocery lifecycle CRM prototype using Python, n8n, Google Sheets, and an LLM. It reads customer history, applies explainable rules to decide whether a customer should receive a first-order, replenishment, repeat-purchase, or win-back draft, suppresses customers without consent or inside a contact cooldown, and logs personalized campaign drafts. I also modelled the KPI layer for conversion, 30-day repeat purchase, campaign cost, attributed revenue, and estimated ROI. The sample data is synthetic, so I present this as a working prototype and a measurement framework—not real lift.”

**Growth questions to discuss:** Which segment has the highest incremental conversion? Does the discount pay for itself after margin? Should replenishment timing vary by category? How do we define a successful second order? How can holdouts distinguish incremental orders from purchases that would have happened anyway? What guardrails prevent over-messaging?

## 12. References and implementation patterns

This project is independently built; these sources informed general integration patterns, not the grocery business rules:

- [n8n documentation](https://docs.n8n.io/) — workflow automation and integrations.
- [n8n Google Sheets node documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlesheets/) — reading, appending, and updating sheet data.
- [n8n AI + Google Sheets example](https://github.com/n8n-io/n8n-docs/blob/main/docs/build/integrate-ai/ai-examples/use-google-sheets-as-a-data-source.md) — using Sheets as an AI workflow data source.
- [Public n8n AI CRM automation example](https://github.com/Bakaare/ai-lead-qualification-n8n) — validation, structured AI output, and spreadsheet logging patterns.
- [Google Sheets API quickstart](https://developers.google.com/workspace/sheets/api/quickstart/python) — Google authentication concepts if extending the project outside n8n.

## License

MIT. See `LICENSE`.
