# Module 01 — Customer Risk Rating Testing

## Objective

This module simulates data-driven testing over the corporate AML customer risk rating process.

The objective is to identify customers whose assigned AML rating may not be consistent with their underlying risk factors.

---

## Why This Matters

The AML lifecycle starts at onboarding.

If the customer risk rating is not correctly assigned, the rest of the AML framework may be weakened. Documentation requirements, enhanced due diligence, restrictive measures, monitoring intensity, escalation and reporting all depend on a reliable risk rating.

A weak rating process can create downstream control failures.

---

## Tests Performed

### 1. High-risk factors but LOW or MEDIUM AML rating

Identifies customers with relevant high-risk indicators but an assigned AML rating that does not appear to reflect those indicators.

Risk indicators include:

* PEP status;
* high-risk geography;
* complex ownership structure;
* adverse media.

---

### 2. PEP customers not classified as HIGH risk

Identifies politically exposed persons whose assigned AML rating is not HIGH.

This may indicate weakness in the risk-based approach, customer due diligence or rating rules.

---

### 3. High-risk geography customers not classified as HIGH risk

Identifies customers linked to high-risk countries whose AML rating is not HIGH.

This may indicate insufficient integration of country risk into the corporate AML rating.

---

### 4. Legal entities with complex ownership not classified as HIGH risk

Identifies legal entities with complex ownership structures that are not rated HIGH.

This may indicate insufficient consideration of beneficial ownership complexity and transparency risk.

---

### 5. Repeated AML issues without rating escalation

Identifies customers with repeated AML-related issues whose rating has not been escalated.

This may indicate weaknesses in ongoing monitoring, periodic review or lifecycle risk reassessment.

---

## Governance Interpretation

Customer risk rating is not a static label.

It is a governance mechanism that determines the level of control applied across the customer lifecycle.

If risk factors change but the rating does not, the institution may apply insufficient due diligence, documentation, monitoring or restrictive measures.

---

## Potential Findings

Potential governance findings may include:

* customer rating not aligned with risk indicators;
* insufficient escalation of repeated AML issues;
* inconsistent application of the risk-based approach;
* weak linkage between adverse media, PEP status, country risk and AML rating;
* lack of integration between onboarding risk factors and lifecycle monitoring.

---

## Recommended Management Actions

Recommended actions may include:

1. Review the corporate AML rating methodology.
2. Validate whether high-risk factors automatically trigger rating review.
3. Strengthen linkage between customer risk factors and rating rules.
4. Review escalation procedures for repeated AML issues.
5. Perform periodic quality assurance over customer risk rating outcomes.
6. Ensure rating changes trigger appropriate documentation, EDD and restrictive measures.

---

## Interview Explanation

I included this module because the AML Lifecycle Transformation role refers specifically to the corporate customer risk rating from onboarding.

The purpose of this module is to show how SQL can be used to test whether the assigned AML rating is consistent with customer risk factors such as PEP status, high-risk geography, complex ownership structures, adverse media and repeated AML issues.

The objective is not to build a full AML rating model, but to demonstrate how data analytics can support AML Governance by identifying inconsistencies, control weaknesses and cases requiring review.
