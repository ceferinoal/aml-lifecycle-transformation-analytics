# Module 02 — Documentation Standards Testing

## Objective

This module simulates data-driven testing over AML documentation standards.

The objective is to identify customers whose documentation package may not be aligned with their AML risk rating, customer type or lifecycle status.

---

## Why This Matters

AML Lifecycle Transformation requires that documentation standards are not applied equally to every customer.

A risk-based approach means that higher-risk customers should normally be subject to stronger documentation requirements, enhanced due diligence and more frequent review.

If documentation standards are not aligned with customer risk, the institution may have weaknesses in onboarding, periodic review, customer due diligence and control effectiveness.

---

## Tests Performed

### 1. HIGH risk customers without Source of Funds documentation

Identifies HIGH risk customers whose source of funds documentation is not valid.

This may indicate insufficient understanding of the origin of the customer’s funds.

---

### 2. Legal entities without Beneficial Ownership documentation

Identifies legal entity customers whose beneficial ownership documentation is not valid.

This may indicate weaknesses in transparency, ownership identification or CDD controls.

---

### 3. HIGH risk customers without Enhanced Due Diligence file

Identifies HIGH risk customers without a valid EDD file.

This may indicate that enhanced due diligence requirements are not being consistently applied.

---

### 4. Active customers with expired KYC documentation

Identifies active customers whose KYC documentation has expired.

This may indicate weaknesses in periodic review, lifecycle monitoring or documentation governance.

---

### 5. HIGH risk customers with incomplete documentation package

Identifies HIGH risk customers with one or more missing or invalid documentation elements.

This may indicate that documentation standards are not being fully applied according to the customer’s risk profile.

---

## Governance Interpretation

Documentation standards are a core part of AML lifecycle management.

The customer risk rating should drive the level of documentation required. If a HIGH risk customer does not have valid documentation, the institution may be applying insufficient controls to a higher-risk relationship.

This is especially relevant for AML Holding functions because corporate standards must be clear, deployable and consistently applied across areas and geographies.

---

## Potential Findings

Potential governance findings may include:

* documentation requirements not aligned with AML risk rating;
* HIGH risk customers without valid source of funds;
* legal entities without valid beneficial ownership documentation;
* active customers with expired KYC documentation;
* EDD requirements not consistently applied;
* lack of linkage between risk rating and documentation standards.

---

## Recommended Management Actions

Recommended actions may include:

1. Review the documentation standards linked to each AML risk rating.
2. Validate whether HIGH risk customers have complete and valid documentation.
3. Strengthen controls over source of funds and beneficial ownership documentation.
4. Implement automated alerts for expired KYC documentation.
5. Review whether EDD requirements are consistently triggered for HIGH risk customers.
6. Monitor documentation gaps through AML governance reporting.

---

## Interview Explanation

I included this module because the AML Lifecycle Transformation role refers to defining corporate standards for actions to be taken according to customer risk, including documentation requirements.

The purpose of this module is to show how SQL can be used to test whether customer documentation is aligned with AML risk rating, customer type and lifecycle status.

The objective is not to perform operational KYC review, but to demonstrate how data analytics can support AML Governance by identifying documentation gaps, control weaknesses and areas requiring remediation.
