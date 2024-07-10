{{
    config(
        materialized='incremental',
        unique_key='code'
    )
}}

WITH
    departement AS (
        SELECT
            version AS version,
            insee_dep AS code,            
            nom AS nom,
            insee_reg AS code_reg,
            long AS long,
            lat AS lat           
        FROM
            {{ source('collecte_cog_carto', 'cog_carto_departement') }}
    )
    SELECT
        *
    FROM
        departement