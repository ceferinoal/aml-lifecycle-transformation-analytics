"""
Project: AML Lifecycle Transformation Analytics
Script: AML Lifecycle Findings Generator

Objective:
Generate AML lifecycle governance findings from synthetic banking data.

This script reads synthetic CSV datasets and produces:
- reports/aml_lifecycle_findings_summary.csv
- reports/aml_lifecycle_governance_report.md

Important:
All data is synthetic. The objective is not to replicate a real AML model,
but to demonstrate how AML/CFT governance logic can be translated into
data-driven tests, findings, prioritisation and executive reporting.
"""

from pathlib import Path
from datetime import date
import pandas as pd


# ============================================================
# Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

TODAY = pd.Timestamp(date.today())


# ============================================================
# Load data
# ============================================================

customers = pd.read_csv(DATA_DIR / "customers.csv")
customer_risk_factors = pd.read_csv(DATA_DIR / "customer_risk_factors.csv")
aml_ratings = pd.read_csv(DATA_DIR / "aml_ratings.csv")
customer_documents = pd.read_csv(DATA_DIR / "customer_documents.csv")
restrictive_measures = pd.read_csv(DATA_DIR / "restrictive_measures.csv")
geography_rollout = pd.read_csv(DATA_DIR / "geography_rollout.csv")
training_communications = pd.read_csv(DATA_DIR / "training_communications.csv")
critical_reports = pd.read_csv(DATA_DIR / "critical_reports.csv")


# ============================================================
# Date conversion
# ============================================================

date_columns = {
    "customers": ["onboarding_date"],
    "aml_ratings": ["last_rating_review_date"],
    "customer_documents": ["kyc_document_expiry_date"],
    "restrictive_measures": ["last_measure_review_date"],
    "geography_rollout": [
        "communication_date",
        "implementation_deadline",
        "actual_implementation_date",
        "remediation_due_date",
    ],
    "training_communications": [
        "training_deadline",
        "communication_date",
        "acknowledgement_due_date",
        "last_training_completion_date",
    ],
    "critical_reports": ["due_date"],
}

for column in date_columns["customers"]:
    customers[column] = pd.to_datetime(customers[column], errors="coerce")

for column in date_columns["aml_ratings"]:
    aml_ratings[column] = pd.to_datetime(aml_ratings[column], errors="coerce")

for column in date_columns["customer_documents"]:
    customer_documents[column] = pd.to_datetime(customer_documents[column], errors="coerce")

for column in date_columns["restrictive_measures"]:
    restrictive_measures[column] = pd.to_datetime(restrictive_measures[column], errors="coerce")

for column in date_columns["geography_rollout"]:
    geography_rollout[column] = pd.to_datetime(geography_rollout[column], errors="coerce")

for column in date_columns["training_communications"]:
    training_communications[column] = pd.to_datetime(training_communications[column], errors="coerce")

for column in date_columns["critical_reports"]:
    critical_reports[column] = pd.to_datetime(critical_reports[column], errors="coerce")


# ============================================================
# Helper functions
# ============================================================

findings = []


def severity_from_count(count: int, high_threshold: int, medium_threshold: int) -> str:
    """Assign severity based on number of affected records."""
    if count >= high_threshold:
        return "HIGH"
    if count >= medium_threshold:
        return "MEDIUM"
    if count > 0:
        return "LOW"
    return "NONE"


def top_dimension_values(df: pd.DataFrame, column: str, top_n: int = 3) -> str:
    """Return top values for a dimension as a readable string."""
    if df.empty or column not in df.columns:
        return "N/A"

    values = df[column].value_counts().head(top_n)
    if values.empty:
        return "N/A"

    return "; ".join([f"{idx}: {val}" for idx, val in values.items()])


def add_finding(
    area: str,
    test_name: str,
    description: str,
    affected_records: int,
    severity: str,
    key_dimension: str,
    governance_impact: str,
    recommended_action: str,
):
    """Append a finding to the findings list."""
    if affected_records > 0:
        findings.append({
            "area": area,
            "test_name": test_name,
            "description": description,
            "affected_records": affected_records,
            "severity": severity,
            "key_dimension": key_dimension,
            "governance_impact": governance_impact,
            "recommended_action": recommended_action,
        })


# ============================================================
# 1. Customer Risk Rating Findings
# ============================================================

rating_data = (
    customers
    .merge(aml_ratings, on="customer_id", how="left")
    .merge(customer_risk_factors, on="customer_id", how="left")
)

rating_inconsistencies = rating_data[
    rating_data["assigned_aml_rating"].isin(["LOW", "MEDIUM"])
    & (
        (rating_data["pep_flag"] == "YES")
        | (rating_data["high_risk_country_flag"] == "YES")
        | (rating_data["complex_ownership_flag"] == "YES")
        | (rating_data["adverse_media_flag"] == "YES")
        | (rating_data["repeated_aml_issues_count"] >= 3)
    )
]

add_finding(
    area="Customer Risk Rating",
    test_name="High-risk factors with LOW/MEDIUM assigned AML rating",
    description=(
        "Customers with relevant AML risk factors were assigned a LOW or MEDIUM AML rating."
    ),
    affected_records=len(rating_inconsistencies),
    severity=severity_from_count(len(rating_inconsistencies), high_threshold=20, medium_threshold=10),
    key_dimension=top_dimension_values(rating_inconsistencies, "country"),
    governance_impact=(
        "Potential misalignment between customer risk factors and corporate AML rating logic."
    ),
    recommended_action=(
        "Review rating assignment rules, perform quality assurance and prioritise remediation for higher-risk customers."
    ),
)

stale_rating_reviews = rating_data[
    rating_data["last_rating_review_date"] < TODAY - pd.DateOffset(months=12)
]

add_finding(
    area="Customer Risk Rating",
    test_name="AML rating review older than 12 months",
    description="Customers have not had their AML rating reviewed within the expected period.",
    affected_records=len(stale_rating_reviews),
    severity=severity_from_count(len(stale_rating_reviews), high_threshold=80, medium_threshold=30),
    key_dimension=top_dimension_values(stale_rating_reviews, "assigned_aml_rating"),
    governance_impact=(
        "Customer AML ratings may not reflect current risk profile or lifecycle changes."
    ),
    recommended_action=(
        "Define rating review frequency by customer risk level and monitor overdue reviews."
    ),
)


# ============================================================
# 2. Documentation Standards Findings
# ============================================================

documentation_data = (
    customers
    .merge(aml_ratings, on="customer_id", how="left")
    .merge(customer_documents, on="customer_id", how="left")
)

high_risk_sof_missing = documentation_data[
    documentation_data["assigned_aml_rating"].isin(["HIGH", "CRITICAL"])
    & (documentation_data["source_of_funds_status"] != "VALID")
]

add_finding(
    area="Documentation Standards",
    test_name="HIGH/CRITICAL customers without valid Source of Funds",
    description="High-risk customers do not have valid Source of Funds documentation.",
    affected_records=len(high_risk_sof_missing),
    severity=severity_from_count(len(high_risk_sof_missing), high_threshold=15, medium_threshold=5),
    key_dimension=top_dimension_values(high_risk_sof_missing, "country"),
    governance_impact=(
        "Documentation requirements may not be aligned with the risk-based approach."
    ),
    recommended_action=(
        "Prioritise remediation of Source of Funds gaps for HIGH and CRITICAL customers."
    ),
)

legal_entity_bo_missing = documentation_data[
    (documentation_data["customer_type"] == "LEGAL_ENTITY")
    & (documentation_data["beneficial_ownership_status"] != "VALID")
]

add_finding(
    area="Documentation Standards",
    test_name="Legal entities without valid Beneficial Ownership documentation",
    description="Legal entity customers do not have valid beneficial ownership documentation.",
    affected_records=len(legal_entity_bo_missing),
    severity=severity_from_count(len(legal_entity_bo_missing), high_threshold=20, medium_threshold=8),
    key_dimension=top_dimension_values(legal_entity_bo_missing, "country"),
    governance_impact=(
        "Weakness in customer ownership transparency and KYC documentation standards."
    ),
    recommended_action=(
        "Review beneficial ownership collection controls and remediation workflow for legal entities."
    ),
)

expired_kyc = documentation_data[
    (documentation_data["customer_status"] == "ACTIVE")
    & (documentation_data["kyc_document_expiry_date"] < TODAY)
]

add_finding(
    area="Documentation Standards",
    test_name="Active customers with expired KYC documentation",
    description="Active customers have expired KYC documentation.",
    affected_records=len(expired_kyc),
    severity=severity_from_count(len(expired_kyc), high_threshold=30, medium_threshold=10),
    key_dimension=top_dimension_values(expired_kyc, "assigned_aml_rating"),
    governance_impact=(
        "Customer lifecycle documentation may not be refreshed in a timely manner."
    ),
    recommended_action=(
        "Implement periodic KYC refresh monitoring and escalation for overdue documentation."
    ),
)


# ============================================================
# 3. Restrictive Measures Findings
# ============================================================

restrictive_data = (
    customers
    .merge(aml_ratings, on="customer_id", how="left")
    .merge(customer_risk_factors, on="customer_id", how="left")
    .merge(restrictive_measures, on="customer_id", how="left")
)

high_risk_without_measure = restrictive_data[
    restrictive_data["assigned_aml_rating"].isin(["HIGH", "CRITICAL"])
    & (
        restrictive_data["restrictive_measure_status"].isna()
        | (restrictive_data["restrictive_measure_status"] == "NOT_APPLIED")
    )
]

add_finding(
    area="Restrictive Measures",
    test_name="HIGH/CRITICAL customers without restrictive measures",
    description="High-risk customers do not have restrictive or enhanced measures applied.",
    affected_records=len(high_risk_without_measure),
    severity=severity_from_count(len(high_risk_without_measure), high_threshold=15, medium_threshold=5),
    key_dimension=top_dimension_values(high_risk_without_measure, "country"),
    governance_impact=(
        "Risk-based measures may not be consistently triggered by AML rating."
    ),
    recommended_action=(
        "Define automatic triggers for enhanced measures and review exceptions with Compliance owners."
    ),
)

adverse_media_without_monitoring = restrictive_data[
    (restrictive_data["adverse_media_flag"] == "YES")
    & (restrictive_data["enhanced_monitoring_flag"] != "YES")
]

add_finding(
    area="Restrictive Measures",
    test_name="Adverse media without enhanced monitoring",
    description="Customers with adverse media do not have enhanced monitoring activated.",
    affected_records=len(adverse_media_without_monitoring),
    severity=severity_from_count(len(adverse_media_without_monitoring), high_threshold=10, medium_threshold=4),
    key_dimension=top_dimension_values(adverse_media_without_monitoring, "country"),
    governance_impact=(
        "Potential weakness in the link between adverse media indicators and ongoing monitoring."
    ),
    recommended_action=(
        "Review adverse media escalation criteria and monitoring activation controls."
    ),
)

stale_measure_reviews = restrictive_data[
    (restrictive_data["restrictive_measure_status"] == "APPLIED")
    & (restrictive_data["last_measure_review_date"] < TODAY - pd.DateOffset(months=12))
]

add_finding(
    area="Restrictive Measures",
    test_name="Restrictive measures not reviewed within 12 months",
    description="Applied restrictive measures have not been reviewed within the expected period.",
    affected_records=len(stale_measure_reviews),
    severity=severity_from_count(len(stale_measure_reviews), high_threshold=20, medium_threshold=8),
    key_dimension=top_dimension_values(stale_measure_reviews, "measure_type"),
    governance_impact=(
        "Restrictive measures may no longer reflect current risk or remediation status."
    ),
    recommended_action=(
        "Define review cycles for restrictive measures and escalate overdue reviews."
    ),
)


# ============================================================
# 4. Geography Rollout Findings
# ============================================================

rollout_not_implemented = geography_rollout[
    geography_rollout["rollout_status"] != "IMPLEMENTED"
]

add_finding(
    area="Geography Rollout",
    test_name="AML lifecycle standard not fully implemented",
    description="Corporate AML lifecycle standards have not been implemented in all geographies.",
    affected_records=len(rollout_not_implemented),
    severity=severity_from_count(len(rollout_not_implemented), high_threshold=5, medium_threshold=2),
    key_dimension=top_dimension_values(rollout_not_implemented, "region"),
    governance_impact=(
        "Corporate AML standards may not be consistently deployed across geographies."
    ),
    recommended_action=(
        "Track implementation status by geography and escalate delayed or not-started rollouts."
    ),
)

rollout_overdue = geography_rollout[
    (geography_rollout["rollout_status"] != "IMPLEMENTED")
    & (geography_rollout["implementation_deadline"] < TODAY)
]

add_finding(
    area="Geography Rollout",
    test_name="Rollout implementation deadline missed",
    description="Geographies have missed AML lifecycle rollout implementation deadlines.",
    affected_records=len(rollout_overdue),
    severity=severity_from_count(len(rollout_overdue), high_threshold=4, medium_threshold=2),
    key_dimension=top_dimension_values(rollout_overdue, "country"),
    governance_impact=(
        "Implementation delays may weaken consistency of AML lifecycle controls."
    ),
    recommended_action=(
        "Assign remediation owners, update implementation plans and monitor overdue actions."
    ),
)

rollout_gaps_open = geography_rollout[
    (geography_rollout["open_gaps_count"] > 0)
    & (geography_rollout["remediation_status"] != "CLOSED")
]

add_finding(
    area="Geography Rollout",
    test_name="Open rollout gaps without closed remediation",
    description="Geographies have open rollout gaps that have not been fully remediated.",
    affected_records=len(rollout_gaps_open),
    severity=severity_from_count(len(rollout_gaps_open), high_threshold=5, medium_threshold=2),
    key_dimension=top_dimension_values(rollout_gaps_open, "region"),
    governance_impact=(
        "Rollout issues may remain unresolved after implementation or communication."
    ),
    recommended_action=(
        "Monitor open gaps through governance reporting until remediation is closed."
    ),
)


# ============================================================
# 5. Training and Communication Findings
# ============================================================

critical_training_incomplete = training_communications[
    (training_communications["critical_area_flag"] == "YES")
    & (training_communications["training_status"] != "COMPLETED")
]

add_finding(
    area="Training & Communication",
    test_name="Critical areas without completed AML lifecycle training",
    description="Critical areas have not completed AML lifecycle training.",
    affected_records=len(critical_training_incomplete),
    severity=severity_from_count(len(critical_training_incomplete), high_threshold=25, medium_threshold=10),
    key_dimension=top_dimension_values(critical_training_incomplete, "business_area"),
    governance_impact=(
        "AML lifecycle standards may not be understood by areas that execute customer processes."
    ),
    recommended_action=(
        "Prioritise mandatory training completion for critical areas and track by business owner."
    ),
)

low_completion_rate = training_communications[
    training_communications["completion_rate"] < 0.80
]

add_finding(
    area="Training & Communication",
    test_name="Low AML training completion rate",
    description="Training initiatives have completion rates below 80%.",
    affected_records=len(low_completion_rate),
    severity=severity_from_count(len(low_completion_rate), high_threshold=20, medium_threshold=8),
    key_dimension=top_dimension_values(low_completion_rate, "country"),
    governance_impact=(
        "Weak adoption of AML lifecycle training may reduce effectiveness of transformation."
    ),
    recommended_action=(
        "Monitor completion by geography and require action plans for low-completion areas."
    ),
)

communications_not_acknowledged = training_communications[
    training_communications["acknowledgement_status"] != "ACKNOWLEDGED"
]

add_finding(
    area="Training & Communication",
    test_name="AML communications not acknowledged",
    description="AML lifecycle communications have not been acknowledged by target areas.",
    affected_records=len(communications_not_acknowledged),
    severity=severity_from_count(len(communications_not_acknowledged), high_threshold=20, medium_threshold=8),
    key_dimension=top_dimension_values(communications_not_acknowledged, "business_area"),
    governance_impact=(
        "Communication may not translate into confirmed awareness or ownership."
    ),
    recommended_action=(
        "Track acknowledgement of AML communications and escalate overdue responses."
    ),
)


# ============================================================
# 6. Critical Reporting Findings
# ============================================================

reports_overdue = critical_reports[
    (critical_reports["submission_status"] != "SUBMITTED")
    & (critical_reports["due_date"] < TODAY)
]

add_finding(
    area="Critical Reporting",
    test_name="Critical AML reports overdue or not submitted",
    description="Critical AML lifecycle reports are overdue or not submitted.",
    affected_records=len(reports_overdue),
    severity=severity_from_count(len(reports_overdue), high_threshold=8, medium_threshold=3),
    key_dimension=top_dimension_values(reports_overdue, "reporting_area"),
    governance_impact=(
        "AML Holding may lack timely visibility over lifecycle risks and remediation status."
    ),
    recommended_action=(
        "Escalate overdue reports and define ownership for report preparation and submission."
    ),
)

high_severity_not_escalated = critical_reports[
    (critical_reports["high_severity_issues_count"] > 0)
    & (critical_reports["escalation_status"] != "ESCALATED")
]

add_finding(
    area="Critical Reporting",
    test_name="High-severity AML issues not escalated",
    description="Critical reports contain high-severity issues that have not been escalated.",
    affected_records=len(high_severity_not_escalated),
    severity=severity_from_count(len(high_severity_not_escalated), high_threshold=5, medium_threshold=2),
    key_dimension=top_dimension_values(high_severity_not_escalated, "reporting_area"),
    governance_impact=(
        "Material AML lifecycle issues may not receive appropriate senior management attention."
    ),
    recommended_action=(
        "Define escalation criteria for high-severity issues and monitor escalation completion."
    ),
)


# ============================================================
# Create findings summary
# ============================================================

findings_summary = pd.DataFrame(findings)

if findings_summary.empty:
    findings_summary = pd.DataFrame(columns=[
        "area",
        "test_name",
        "description",
        "affected_records",
        "severity",
        "key_dimension",
        "governance_impact",
        "recommended_action",
    ])

findings_summary = findings_summary.sort_values(
    by=["severity", "affected_records"],
    ascending=[True, False],
)

severity_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3, "NONE": 4}
findings_summary["severity_order"] = findings_summary["severity"].map(severity_order)
findings_summary = findings_summary.sort_values(
    by=["severity_order", "affected_records"],
    ascending=[True, False],
).drop(columns=["severity_order"])

summary_path = REPORTS_DIR / "aml_lifecycle_findings_summary.csv"
findings_summary.to_csv(summary_path, index=False)


# ============================================================
# Create executive governance report
# ============================================================

total_findings = len(findings_summary)
total_affected_records = int(findings_summary["affected_records"].sum()) if total_findings else 0

severity_counts = (
    findings_summary["severity"]
    .value_counts()
    .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
)

area_summary = (
    findings_summary
    .groupby("area", as_index=False)
    .agg(
        findings_count=("test_name", "count"),
        affected_records=("affected_records", "sum")
    )
    .sort_values("affected_records", ascending=False)
)

high_priority = findings_summary[
    findings_summary["severity"].isin(["HIGH", "MEDIUM"])
].copy()


def dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    """Convert dataframe to markdown table without requiring external libraries."""
    if df.empty:
        return "No records."

    headers = list(df.columns)
    rows = df.astype(str).values.tolist()

    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = [
        "| " + " | ".join(row) + " |"
        for row in rows
    ]

    return "\n".join([header_line, separator_line] + row_lines)


executive_summary_table = findings_summary[
    [
        "area",
        "test_name",
        "affected_records",
        "severity",
        "key_dimension",
    ]
].copy()

area_summary_table = area_summary.copy()

high_priority_table = high_priority[
    [
        "area",
        "test_name",
        "affected_records",
        "severity",
        "governance_impact",
        "recommended_action",
    ]
].copy()

report_content = f"""# AML Lifecycle Governance Report

## Executive Summary

This report consolidates data-driven findings from the AML Lifecycle Transformation Analytics project.

The objective is to show how AML/CFT lifecycle requirements can be translated into control testing, exception identification, prioritisation and governance reporting.

All data used in this report is synthetic.

---

## Key Metrics

- Total findings identified: **{total_findings}**
- Total affected records across findings: **{total_affected_records}**
- HIGH severity findings: **{severity_counts.get("HIGH", 0)}**
- MEDIUM severity findings: **{severity_counts.get("MEDIUM", 0)}**
- LOW severity findings: **{severity_counts.get("LOW", 0)}**

---

## Findings by Area

{dataframe_to_markdown_table(area_summary_table)}

---

## Executive Findings Summary

{dataframe_to_markdown_table(executive_summary_table)}

---

## High and Medium Priority Findings

{dataframe_to_markdown_table(high_priority_table)}

---

## Governance Interpretation

The findings indicate how weaknesses in AML lifecycle execution may appear across multiple layers:

- customer risk rating;
- customer documentation standards;
- restrictive and enhanced measures;
- geography rollout;
- training and communication;
- critical reporting.

The value of this analysis is not only identifying isolated exceptions, but creating visibility over where AML lifecycle governance may require stronger ownership, escalation and remediation.

---

## Management Actions

Recommended management actions include:

1. Prioritise HIGH severity findings for immediate review.
2. Assign clear ownership for remediation by area and geography.
3. Monitor recurring gaps through standard AML lifecycle KRIs.
4. Link customer risk rating, documentation and restrictive measures into a single governance view.
5. Track training, communication and acknowledgement as evidence of organisational adoption.
6. Escalate overdue reports and high-severity issues through the appropriate governance forums.

---

## Professional Positioning

This report demonstrates the ability to connect AML/CFT regulation, customer lifecycle controls, governance logic, data analytics and executive reporting.

The purpose is to show how an AML Lifecycle Transformation or Financial Crime Governance function can use data to move from policy definition to control visibility, prioritisation and remediation.
"""

report_path = REPORTS_DIR / "aml_lifecycle_governance_report.md"
report_path.write_text(report_content, encoding="utf-8")


# ============================================================
# Console output
# ============================================================

print("AML lifecycle findings generated successfully.")
print(f"- {summary_path}")
print(f"- {report_path}")
print("")
print("Findings by severity:")
print(severity_counts.to_string())
print("")
print("Findings by area:")
print(area_summary.to_string(index=False))