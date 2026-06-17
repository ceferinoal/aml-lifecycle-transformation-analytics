# Module 03 — Restrictive Measures Testing

## Objective

This module simulates data-driven testing over AML restrictive and enhanced measures.

The objective is to identify customers whose risk profile may require restrictive measures, enhanced monitoring, onboarding limitations or escalation, but where those measures have not been applied or reviewed.

---

## Why This Matters

AML Lifecycle Transformation does not end with assigning a customer risk rating.

The rating must trigger appropriate actions.

For higher-risk customers, this may include enhanced due diligence, additional documentation, onboarding restrictions, transactional limitations, enhanced monitoring or escalation to Compliance.

If restrictive measures are not aligned with the customer’s risk profile, the institution may have a gap between policy and operational execution.

---

## Tests Performed

### 1. HIGH risk customers without any restrictive measure

Identifies HIGH risk customers with no restrictive measure applied.

This may indicate that the customer risk rating is not properly connected to downstream AML controls.

---

### 2. Customers with adverse media but no enhanced monitoring

Identifies customers with adverse media indicators but no enhanced monitoring.

This may indicate insufficient response to reputational or financial crime risk signals.

---

### 3. Customers with incomplete documentation but no onboarding restriction

Identifies active customers with incomplete or invalid documentation where no onboarding restriction has been applied.

This may indicate that documentation gaps are not triggering appropriate lifecycle controls.

---

### 4. Critical AML rating without escalation requirement

Identifies customers with a CRITICAL AML rating but no escalation requirement.

This may indicate weaknesses in escalation governance or lack of linkage between rating and mandatory actions.

---

### 5. Restrictive measures applied but not reviewed

Identifies restrictive measures that have been applied but not reviewed within the expected period.

This may indicate weaknesses in ongoing monitoring and lifecycle governance.

---

## Governance Interpretation

Restrictive measures are a key part of AML lifecycle management.

A risk-based approach requires that higher-risk customers receive stronger controls and that those controls are reviewed periodically.

From an AML Holding perspective, the key issue is not only whether restrictive measures exist, but whether they are consistently triggered, documented, reviewed and deployed across the organization.

---

## Potential Findings

Potential governance findings may include:

* restrictive measures not aligned with customer AML rating;
* high-risk customers without enhanced controls;
* adverse media not triggering enhanced monitoring;
* incomplete documentation not triggering onboarding restrictions;
* critical-risk customers without escalation;
* restrictive measures not reviewed within the expected period.

---

## Recommended Management Actions

Recommended actions may include:

1. Define clear triggers for restrictive measures based on AML risk rating.
2. Ensure adverse media and documentation gaps trigger appropriate review.
3. Link critical ratings to mandatory escalation workflows.
4. Monitor restrictive measures through governance reporting.
5. Define periodic review requirements for applied measures.
6. Track overdue reviews and unresolved restrictive measure gaps.

---

## Interview Explanation

I included this module because the AML Lifecycle Transformation role refers to defining corporate standards for actions to be taken according to customer risk, including restrictive measures.

The purpose of this module is to show how SQL can be used to test whether higher-risk customers have appropriate restrictive or enhanced measures applied.

The objective is not to perform operational case investigation, but to demonstrate how data analytics can support AML Governance by identifying gaps between risk rating, documentation status, adverse media and the actions applied across the customer lifecycle.
