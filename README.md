# AML Lifecycle Transformation Analytics

## Project Overview

This project simulates an AML Lifecycle Transformation framework using synthetic banking data, SQL and Python.

The objective is to demonstrate how AML Holding, Compliance and Financial Crime Governance teams can use data analytics to review customer lifecycle controls, corporate AML risk rating, KYC/CDD/EDD documentation standards, restrictive measures, rollout across geographies, training, communication and critical reporting.

The project is aligned with a governance and transformation perspective, not with operational alert handling.

It focuses on how AML/CFT requirements can be translated into:

* customer risk rating logic;
* KYC/CDD/EDD documentation standards;
* risk-based restrictive measures;
* rollout monitoring across geographies;
* training and communication tracking;
* critical governance reporting;
* findings identification;
* remediation prioritisation;
* executive AML lifecycle reporting.

---

## Business Context

AML/CFT risk is not only managed through transaction monitoring.

A strong AML framework starts at onboarding and continues throughout the customer lifecycle. Financial institutions need to know their customers, assign appropriate AML risk ratings, request documentation based on risk, apply enhanced or restrictive measures when required, ensure consistent rollout across geographies and produce reliable governance reporting.

A corporate AML standard only creates value if it is:

1. clearly defined;
2. properly communicated;
3. consistently implemented;
4. monitored through controls;
5. supported by evidence;
6. escalated when material gaps appear.

This project simulates that lifecycle.

---

## What This Project Demonstrates

This repository demonstrates the ability to connect:

* AML/CFT regulation;
* customer lifecycle management;
* corporate risk rating;
* KYC/CDD/EDD controls;
* documentation standards;
* restrictive and enhanced measures;
* governance reporting;
* transformation rollout;
* data analytics;
* control testing;
* findings generation;
* executive-level reporting.

The purpose is not to replicate a real AML model or a real bank framework.

The purpose is to show how AML lifecycle governance logic can be translated into data-driven tests, exception identification and reporting outputs.

---

## Repository Structure

```text
aml-lifecycle-transformation-analytics/
│
├── data/
│   ├── customers.csv
│   ├── customer_risk_factors.csv
│   ├── aml_ratings.csv
│   ├── customer_documents.csv
│   ├── restrictive_measures.csv
│   ├── geography_rollout.csv
│   ├── training_communications.csv
│   └── critical_reports.csv
│
├── sql/
│   ├── 01_customer_risk_rating_testing.sql
│   ├── 02_documentation_standards_testing.sql
│   ├── 03_restrictive_measures_testing.sql
│   ├── 04_geography_rollout_testing.sql
│   ├── 05_training_communication_testing.sql
│   └── 06_critical_reporting_testing.sql
│
├── python/
│   ├── 01_generate_synthetic_aml_lifecycle_data.py
│   └── 02_generate_aml_lifecycle_findings.py
│
├── reports/
│   ├── 01_customer_risk_rating_explanation.md
│   ├── 02_documentation_standards_explanation.md
│   ├── 03_restrictive_measures_explanation.md
│   ├── 04_geography_rollout_explanation.md
│   ├── 05_training_communication_explanation.md
│   ├── 06_critical_reporting_explanation.md
│   ├── aml_lifecycle_findings_summary.csv
│   └── aml_lifecycle_governance_report.md
│
├── requirements.txt
└── README.md
```

---

## Project Modules

### 1. Customer Risk Rating Testing

Tests whether the assigned AML rating is consistent with customer risk factors such as PEP status, high-risk geography, complex ownership structures, adverse media and repeated AML issues.

This module reflects the idea that customer risk rating is not just a label, but the starting point of the AML customer lifecycle.

---

### 2. Documentation Standards Testing

Tests whether customer documentation requirements are aligned with the customer’s AML risk level.

The module reviews documentation areas such as identity documentation, source of funds, beneficial ownership and enhanced due diligence files.

---

### 3. Restrictive Measures Testing

Tests whether enhanced measures, restrictions or controls are applied when the customer risk profile requires them.

This module links AML rating, adverse media, documentation gaps and escalation logic to risk-based measures.

---

### 4. Geography Rollout Testing

Tests whether AML lifecycle standards are consistently deployed across different geographies.

The module reviews implementation status, ownership, deadlines, remediation gaps and post-implementation issues.

---

### 5. Training & Communication Testing

Tests whether relevant areas have received, acknowledged and completed AML lifecycle training and communications.

This module reflects the importance of embedding AML standards into the organization, especially across Business, Compliance, Risk, Engineering, Operations and Customer Onboarding teams.

---

### 6. Critical Reporting Testing

Consolidates key exceptions into governance indicators for AML Holding, Compliance and senior management reporting.

This module simulates how fragmented AML lifecycle issues can be transformed into structured reporting, prioritisation and escalation.

---

## Data

All datasets are synthetic.

The synthetic data includes:

* customers;
* customer risk factors;
* AML ratings;
* customer documentation;
* restrictive measures;
* geography rollout records;
* training and communication records;
* critical reporting records.

The data intentionally includes inconsistencies and exceptions in order to support control testing and findings generation.

---

## How to Run the Project

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Generate synthetic data

```bash
python python/01_generate_synthetic_aml_lifecycle_data.py
```

This creates the CSV files inside the `data/` folder.

### 3. Generate findings and governance report

```bash
python python/02_generate_aml_lifecycle_findings.py
```

This creates:

```text
reports/aml_lifecycle_findings_summary.csv
reports/aml_lifecycle_governance_report.md
```

---

## Outputs

The project produces two main executive outputs:

### AML Lifecycle Findings Summary

File:

```text
reports/aml_lifecycle_findings_summary.csv
```

This file consolidates findings by:

* area;
* test name;
* description;
* affected records;
* severity;
* key dimension;
* governance impact;
* recommended action.

---

### AML Lifecycle Governance Report

File:

```text
reports/aml_lifecycle_governance_report.md
```

This report provides an executive-level view of:

* total findings;
* affected records;
* severity distribution;
* findings by area;
* high and medium priority issues;
* governance interpretation;
* recommended management actions.

---

## Example Governance Questions Addressed

This project helps answer questions such as:

* Are customer AML ratings aligned with risk factors?
* Are high-risk customers supported by appropriate KYC/CDD/EDD documentation?
* Are restrictive or enhanced measures applied when required?
* Are corporate AML lifecycle standards consistently rolled out across geographies?
* Are critical areas trained and informed about customer knowledge requirements?
* Are material AML lifecycle issues escalated and reported appropriately?
* Can fragmented exceptions be consolidated into governance indicators?

---

## Tools Used

* SQL
* Python
* Pandas
* NumPy
* Synthetic banking data
* AML/CFT governance logic
* Risk-based approach
* Customer lifecycle controls
* Findings generation
* Executive reporting

---

## Important Disclaimer

All data used in this project is synthetic.

This project does not use, represent or reproduce real customer data, real bank data or confidential information from any financial institution.

The purpose is not to replicate a real AML model, issue regulatory conclusions or substitute professional judgement.

Final AML conclusions would always require:

* regulatory context;
* review of internal policies and procedures;
* validation with process owners;
* subject matter expert judgement;
* governance approval;
* evidence review.

---

## Professional Positioning

This project reflects a governance-oriented AML profile.

It is designed to show the ability to connect:

* AML/CFT regulation;
* customer lifecycle;
* corporate risk rating;
* KYC/CDD/EDD;
* internal controls;
* reporting;
* transformation;
* data analytics;
* governance thinking.

The objective is not to act as an AML operations analyst, but to demonstrate how data can support AML Lifecycle Transformation, Financial Crime Governance and risk-based decision-making.

The project shows how AML/CFT requirements can be translated into control logic, data testing, findings, remediation priorities and executive reporting.


