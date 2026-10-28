# Demo run summary

- **Evaluation date:** 2026-10-27
- **Customer records evaluated:** 1,000
- **Campaign drafts queued:** 668
- **Customers suppressed:** 332
- **Actual sends performed:** 0 (draft-only safety mode)
- **Data note:** campaign performance metrics use simulated historical rows and are not real results.

## Suppression reasons

- `campaign_cooldown`: 156
- `no_marketing_consent`: 176

## Campaign queue by segment

| Segment | Campaign type | Drafts |
|---|---|---:|
| Active Customer Nurture | Relevant Category Nurture | 136 |
| Active Repeat Customer | Cross-Sell & Habit | 125 |
| Dormant Repeat Customer | Win-Back | 89 |
| Dormant Signup | First Order Activation | 55 |
| First-Order Customer | Post-Purchase Reorder | 50 |
| High-Value At-Risk | VIP Re-engagement | 35 |
| High-Value Win-Back | Win-Back | 6 |
| New Signup | First Order Activation | 6 |
| One-Time Buyer | First-to-Second Order | 88 |
| Replenishment Due | Replenishment Reminder | 78 |

## KPI notes

Open `kpi_report.json` for simulated delivery, open, click, conversion, repeat-purchase, revenue and estimated ROI metrics. Replace the assumed gross margin and attribution logic before using these calculations in a real business.
