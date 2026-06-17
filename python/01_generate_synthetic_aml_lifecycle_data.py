"""
Project: AML Lifecycle Transformation Analytics
Script: Synthetic AML Lifecycle Data Generator

Objective:
Generate synthetic banking data to simulate AML Lifecycle Transformation testing.

The generated datasets support SQL testing over:
- Customer risk rating
- Documentation standards
- Restrictive measures
- Geography rollout
- Training and communication
- Critical reporting

Important:
All data is synthetic. It does not represent real customers, real BBVA data,
or any real financial institution.
"""

from pathlib import Path
from datetime import date, timedelta
import numpy as np
import pandas as pd


# ============================================================
# Configuration
# ============================================================

np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

TODAY = date.today()

COUNTRIES = [
    "Spain", "Mexico", "Colombia", "Peru", "Argentina",
    "Turkey", "Morocco", "Panama", "UAE", "Switzerland"
]

HIGH_RISK_COUNTRIES = ["Panama", "UAE", "Turkey"]

REGIONS = {
    "Spain": "Europe",
    "Switzerland": "Europe",
    "Mexico": "North America",
    "Colombia": "South America",
    "Peru": "South America",
    "Argentina": "South America",
    "Turkey": "EMEA",
    "Morocco": "Africa",
    "Panama": "Central America",
    "UAE": "Middle East",
}

BUSINESS_AREAS = [
    "Retail Banking",
    "Corporate Banking",
    "Compliance",
    "Risk",
    "Engineering",
    "Operations",
    "Customer Onboarding",
]


# ============================================================
# Helper functions
# ============================================================

def random_past_date(min_days: int, max_days: int) -> str:
    days = int(np.random.randint(min_days, max_days))
    return (TODAY - timedelta(days=days)).isoformat()


def random_future_date(min_days: int, max_days: int) -> str:
    days = int(np.random.randint(min_days, max_days))
    return (TODAY + timedelta(days=days)).isoformat()


def yes_no(prob_yes: float) -> str:
    return "YES" if np.random.rand() < prob_yes else "NO"


def valid_invalid(prob_valid: float) -> str:
    return "VALID" if np.random.rand() < prob_valid else "INVALID"


# ============================================================
# 1. Customers
# ============================================================

num_customers = 250

customer_ids = [f"CUST_{str(i).zfill(4)}" for i in range(1, num_customers + 1)]

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "customer_type": np.random.choice(
        ["INDIVIDUAL", "LEGAL_ENTITY"],
        size=num_customers,
        p=[0.72, 0.28]
    ),
    "country": np.random.choice(COUNTRIES, size=num_customers),
    "customer_status": np.random.choice(
        ["ACTIVE", "INACTIVE"],
        size=num_customers,
        p=[0.88, 0.12]
    ),
    "onboarding_date": [
        random_past_date(90, 1800) for _ in range(num_customers)
    ],
})

customers["region"] = customers["country"].map(REGIONS)


# ============================================================
# 2. Customer risk factors
# ============================================================

risk_factors = []

for _, row in customers.iterrows():
    country = row["country"]
    customer_type = row["customer_type"]

    high_risk_country_flag = "YES" if country in HIGH_RISK_COUNTRIES else yes_no(0.05)
    pep_flag = yes_no(0.07)
    complex_ownership_flag = (
        yes_no(0.35) if customer_type == "LEGAL_ENTITY" else "NO"
    )
    adverse_media_flag = yes_no(0.10)
    repeated_aml_issues_count = int(np.random.choice(
        [0, 0, 0, 1, 1, 2, 3, 4, 5],
        p=[0.35, 0.20, 0.10, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02]
    ))

    risk_factors.append({
        "customer_id": row["customer_id"],
        "pep_flag": pep_flag,
        "high_risk_country_flag": high_risk_country_flag,
        "complex_ownership_flag": complex_ownership_flag,
        "adverse_media_flag": adverse_media_flag,
        "repeated_aml_issues_count": repeated_aml_issues_count,
    })

customer_risk_factors = pd.DataFrame(risk_factors)


# ============================================================
# 3. AML ratings
# ============================================================

ratings = []

for _, row in customer_risk_factors.iterrows():
    risk_score = 0

    if row["pep_flag"] == "YES":
        risk_score += 3
    if row["high_risk_country_flag"] == "YES":
        risk_score += 2
    if row["complex_ownership_flag"] == "YES":
        risk_score += 2
    if row["adverse_media_flag"] == "YES":
        risk_score += 2
    if row["repeated_aml_issues_count"] >= 3:
        risk_score += 2

    if risk_score >= 6:
        expected_rating = "CRITICAL"
    elif risk_score >= 3:
        expected_rating = "HIGH"
    elif risk_score >= 1:
        expected_rating = "MEDIUM"
    else:
        expected_rating = "LOW"

    # Intentional inconsistencies for testing purposes
    if np.random.rand() < 0.18 and expected_rating in ["HIGH", "CRITICAL"]:
        assigned_rating = np.random.choice(["LOW", "MEDIUM"])
    elif np.random.rand() < 0.08 and expected_rating == "MEDIUM":
        assigned_rating = "LOW"
    else:
        assigned_rating = expected_rating

    ratings.append({
        "customer_id": row["customer_id"],
        "expected_aml_rating": expected_rating,
        "assigned_aml_rating": assigned_rating,
        "last_rating_review_date": random_past_date(30, 900),
    })

aml_ratings = pd.DataFrame(ratings)


# ============================================================
# 4. Customer documents
# ============================================================

documents = []

for _, customer in customers.iterrows():
    customer_id = customer["customer_id"]
    customer_type = customer["customer_type"]

    rating = aml_ratings.loc[
        aml_ratings["customer_id"] == customer_id,
        "assigned_aml_rating"
    ].iloc[0]

    if rating in ["HIGH", "CRITICAL"]:
        identity_prob = 0.92
        source_of_funds_prob = 0.75
        edd_prob = 0.70
        bo_prob = 0.75
    elif rating == "MEDIUM":
        identity_prob = 0.95
        source_of_funds_prob = 0.82
        edd_prob = 0.55
        bo_prob = 0.80
    else:
        identity_prob = 0.98
        source_of_funds_prob = 0.90
        edd_prob = 0.40
        bo_prob = 0.85

    beneficial_ownership_status = (
        valid_invalid(bo_prob) if customer_type == "LEGAL_ENTITY" else "NOT_APPLICABLE"
    )

    # Some expired documentation is intentionally generated
    if np.random.rand() < 0.18:
        expiry_date = random_past_date(1, 365)
    else:
        expiry_date = random_future_date(30, 730)

    documents.append({
        "customer_id": customer_id,
        "identity_document_status": valid_invalid(identity_prob),
        "source_of_funds_status": valid_invalid(source_of_funds_prob),
        "beneficial_ownership_status": beneficial_ownership_status,
        "edd_file_status": valid_invalid(edd_prob),
        "kyc_document_expiry_date": expiry_date,
    })

customer_documents = pd.DataFrame(documents)


# ============================================================
# 5. Restrictive measures
# ============================================================

restrictive_measures = []

for _, customer in customers.iterrows():
    customer_id = customer["customer_id"]

    rating = aml_ratings.loc[
        aml_ratings["customer_id"] == customer_id,
        "assigned_aml_rating"
    ].iloc[0]

    factors = customer_risk_factors.loc[
        customer_risk_factors["customer_id"] == customer_id
    ].iloc[0]

    should_have_measure = (
        rating in ["HIGH", "CRITICAL"]
        or factors["adverse_media_flag"] == "YES"
        or factors["repeated_aml_issues_count"] >= 3
    )

    if should_have_measure:
        applied_prob = 0.72
    else:
        applied_prob = 0.18

    measure_applied = np.random.rand() < applied_prob

    restrictive_measures.append({
        "customer_id": customer_id,
        "restrictive_measure_status": "APPLIED" if measure_applied else "NOT_APPLIED",
        "measure_type": np.random.choice([
            "ENHANCED_MONITORING",
            "ONBOARDING_RESTRICTION",
            "TRANSACTION_LIMITATION",
            "COMPLIANCE_ESCALATION",
            "NONE"
        ]),
        "enhanced_monitoring_flag": "YES" if measure_applied and np.random.rand() < 0.80 else "NO",
        "onboarding_restriction_flag": "YES" if measure_applied and np.random.rand() < 0.45 else "NO",
        "escalation_required_flag": "YES" if rating == "CRITICAL" and np.random.rand() < 0.80 else "NO",
        "last_measure_review_date": random_past_date(30, 900),
    })

restrictive_measures = pd.DataFrame(restrictive_measures)


# ============================================================
# 6. Geography rollout
# ============================================================

rollout_records = []

for i, country in enumerate(COUNTRIES, start=1):
    status = np.random.choice(
        ["IMPLEMENTED", "IN_PROGRESS", "DELAYED", "NOT_STARTED"],
        p=[0.55, 0.22, 0.15, 0.08]
    )

    deadline = (
        random_past_date(10, 240)
        if status in ["DELAYED", "NOT_STARTED"]
        else random_future_date(30, 240)
    )

    actual_date = (
        random_past_date(10, 180)
        if status == "IMPLEMENTED"
        else ""
    )

    open_gaps = int(np.random.choice([0, 1, 2, 3, 4], p=[0.45, 0.20, 0.18, 0.10, 0.07]))

    rollout_records.append({
        "geography_id": f"GEO_{str(i).zfill(3)}",
        "country": country,
        "region": REGIONS[country],
        "aml_standard_name": "AML Customer Lifecycle Corporate Standard",
        "corporate_standard_version": "v1.0",
        "communication_date": random_past_date(30, 300),
        "rollout_status": status,
        "implementation_deadline": deadline,
        "actual_implementation_date": actual_date,
        "local_owner": np.random.choice(["Local Compliance", "Country MLRO", "Risk Owner", ""]),
        "local_owner_assigned_flag": yes_no(0.85),
        "open_gaps_count": open_gaps,
        "remediation_due_date": random_past_date(5, 180) if open_gaps > 0 else random_future_date(30, 180),
        "remediation_status": np.random.choice(
            ["OPEN", "IN_PROGRESS", "CLOSED"],
            p=[0.25, 0.35, 0.40]
        ),
    })

geography_rollout = pd.DataFrame(rollout_records)


# ============================================================
# 7. Training and communications
# ============================================================

training_records = []

for i in range(1, 71):
    country = np.random.choice(COUNTRIES)
    business_area = np.random.choice(BUSINESS_AREAS)

    completion_rate = round(float(np.random.beta(5, 2)), 2)
    if np.random.rand() < 0.18:
        completion_rate = round(float(np.random.uniform(0.35, 0.79)), 2)

    training_status = "COMPLETED" if completion_rate >= 0.95 else np.random.choice(
        ["IN_PROGRESS", "NOT_COMPLETED"],
        p=[0.65, 0.35]
    )

    training_records.append({
        "training_id": f"TRN_{str(i).zfill(4)}",
        "communication_id": f"COM_{str(i).zfill(4)}",
        "country": country,
        "region": REGIONS[country],
        "business_area": business_area,
        "target_population": int(np.random.randint(20, 500)),
        "critical_area_flag": "YES" if business_area in [
            "Customer Onboarding", "Compliance", "Operations", "Corporate Banking"
        ] else yes_no(0.30),
        "training_name": "AML Customer Lifecycle Standard Training",
        "training_status": training_status,
        "completion_rate": completion_rate,
        "training_deadline": random_past_date(1, 120) if training_status != "COMPLETED" else random_future_date(30, 200),
        "communication_topic": "AML Lifecycle Transformation Update",
        "communication_date": random_past_date(20, 250),
        "acknowledgement_status": np.random.choice(
            ["ACKNOWLEDGED", "NOT_ACKNOWLEDGED"],
            p=[0.78, 0.22]
        ),
        "acknowledgement_due_date": random_past_date(1, 90),
        "onboarding_involved_flag": "YES" if business_area in [
            "Customer Onboarding", "Retail Banking", "Corporate Banking"
        ] else "NO",
        "last_training_completion_date": random_past_date(30, 900),
    })

training_communications = pd.DataFrame(training_records)


# ============================================================
# 8. Critical reports
# ============================================================

critical_reports_list = []

reporting_areas = [
    "Customer Risk Rating",
    "Documentation Standards",
    "Restrictive Measures",
    "Geography Rollout",
    "Training & Communication",
    "AML Lifecycle Governance",
]

for i in range(1, 25):
    open_issues = int(np.random.choice([0, 1, 2, 3, 4, 5], p=[0.30, 0.20, 0.18, 0.14, 0.10, 0.08]))
    high_severity = int(np.random.choice([0, 0, 1, 2], p=[0.55, 0.20, 0.18, 0.07]))

    critical_reports_list.append({
        "report_id": f"REP_{str(i).zfill(4)}",
        "report_name": np.random.choice([
            "Monthly AML Lifecycle Governance Report",
            "Customer Risk Rating Quality Report",
            "KYC Documentation Gap Report",
            "Restrictive Measures Escalation Report",
            "Geography Rollout Status Report",
        ]),
        "reporting_area": np.random.choice(reporting_areas),
        "report_owner": np.random.choice([
            "AML Holding",
            "Compliance Governance",
            "Financial Crime Risk",
            "Local Compliance"
        ]),
        "reporting_frequency": np.random.choice(["MONTHLY", "QUARTERLY"]),
        "due_date": random_past_date(1, 120),
        "submission_status": np.random.choice(
            ["SUBMITTED", "NOT_SUBMITTED", "DRAFT"],
            p=[0.68, 0.18, 0.14]
        ),
        "escalation_status": np.random.choice(
            ["ESCALATED", "NOT_ESCALATED"],
            p=[0.62, 0.38]
        ),
        "open_issues_count": open_issues,
        "high_severity_issues_count": high_severity,
    })

critical_reports = pd.DataFrame(critical_reports_list)


# ============================================================
# Save CSV files
# ============================================================

datasets = {
    "customers.csv": customers,
    "customer_risk_factors.csv": customer_risk_factors,
    "aml_ratings.csv": aml_ratings,
    "customer_documents.csv": customer_documents,
    "restrictive_measures.csv": restrictive_measures,
    "geography_rollout.csv": geography_rollout,
    "training_communications.csv": training_communications,
    "critical_reports.csv": critical_reports,
}

for filename, dataframe in datasets.items():
    output_path = DATA_DIR / filename
    dataframe.to_csv(output_path, index=False)

print("Synthetic AML lifecycle datasets generated successfully.")
print(f"Data folder: {DATA_DIR}")

for filename in datasets:
    print(f"- {filename}")