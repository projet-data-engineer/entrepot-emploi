{{
    config(
        materialized='incremental',
        unique_key='code'
    )
}}

WITH
    commune_arm AS (
        SELECT
            version AS version,
            insee_com AS code,
            insee_com AS code_parent,
            insee_dep AS code_dep,
            insee_reg AS code_reg,
            nom AS nom,
            population AS population,
            long AS long,
            lat AS lat  
        FROM
            {{ source('collecte_cog_carto', 'cog_carto_commune') }}
        UNION
        SELECT
            version AS version,
            insee_arm AS code,
            insee_com AS code_parent,
            null AS code_dep,
            null AS code_reg,
            nom AS nom,
            population AS population,
            long AS long,
            lat AS lat  
        FROM
            {{ source('collecte_cog_carto', 'cog_carto_arrondissement_municipal') }}
    )

    SELECT
        *
    FROM
        commune_arm AS c