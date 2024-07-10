WITH
    region AS (
        SELECT
            version AS version,
            insee_reg AS code,            
            nom AS nom,
            long AS long,
            lat AS lat            
        FROM
            {{ source('collecte_cog_carto', 'cog_carto_region') }}
    )
    SELECT
        *
    FROM
        region