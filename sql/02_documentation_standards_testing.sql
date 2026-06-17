/*
Project: AML Lifecycle Transformation Analytics
Module 02: Documentation Standards Testing

Objective:
Identify potential gaps between customer AML risk rating and the documentation required or collected.

Context:
AML Lifecycle Transformation requires that documentation standards are aligned with the customer risk profile.
Higher-risk customers should normally be subject to stronger documentation, enhanced due diligence and periodic review requirements.
*/

-- ============================================================
-- Test 1: HIGH risk customers without Source of Funds documentation
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    d.source_of_funds_status
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_documents d
    ON c.customer_id = d.customer_id
WHERE r.assigned_aml_rating = 'HIGH'
  AND d.source_of_funds_status <> 'VALID';


-- ============================================================
-- Test 2: Legal entities without Beneficial Ownership documentation
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    d.beneficial_ownership_status
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_documents d
    ON c.customer_id = d.customer_id
WHERE c.customer_type = 'LEGAL_ENTITY'
  AND d.beneficial_ownership_status <> 'VALID';


-- ============================================================
-- Test 3: HIGH risk customers without Enhanced Due Diligence file
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    d.edd_file_status
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_documents d
    ON c.customer_id = d.customer_id
WHERE r.assigned_aml_rating = 'HIGH'
  AND d.edd_file_status <> 'VALID';


-- ============================================================
-- Test 4: Active customers with expired KYC documentation
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    c.customer_status,
    r.assigned_aml_rating,
    d.kyc_document_expiry_date
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_documents d
    ON c.customer_id = d.customer_id
WHERE c.customer_status = 'ACTIVE'
  AND d.kyc_document_expiry_date < CURRENT_DATE;


-- ============================================================
-- Test 5: HIGH risk customers with incomplete documentation package
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    d.identity_document_status,
    d.source_of_funds_status,
    d.beneficial_ownership_status,
    d.edd_file_status
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_documents d
    ON c.customer_id = d.customer_id
WHERE r.assigned_aml_rating = 'HIGH'
  AND (
        d.identity_document_status <> 'VALID'
        OR d.source_of_funds_status <> 'VALID'
        OR d.edd_file_status <> 'VALID'
        OR (
            c.customer_type = 'LEGAL_ENTITY'
            AND d.beneficial_ownership_status <> 'VALID'
        )
      );