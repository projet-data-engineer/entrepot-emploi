{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

WITH offre AS (

    SELECT * FROM {{ source('collecte_offre_emploi', 'offre_emploi') }}
)

SELECT
    id,
    date_creation,
    lieu_travail_code,
    code_naf,
    code_rome,
    entreprise_adaptee,
    type_contrat,
    nature_contrat,
    experience_exige,
    alternance,
    nombre_postes,
    accessible_TH,
    qualification_code
FROM
    offre