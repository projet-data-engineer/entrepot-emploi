WITH
    hierarchie AS (
        SELECT
            niv1,
            niv2,
            niv3,
            niv4,
            niv5
        FROM
            {{ source('collecte_naf', 'naf2008_5_niveaux') }}
    ),
    niveau_1 AS (
        SELECT
            code,
            libelle
        FROM
            {{ source('collecte_naf', 'naf2008_liste_n1') }}
    ),
    niveau_2 AS (
        SELECT
            code,
            libelle
        FROM
            {{ source('collecte_naf', 'naf2008_liste_n2') }}
    ),
    niveau_3 AS (
        SELECT
            code,
            libelle
        FROM
            {{ source('collecte_naf', 'naf2008_liste_n3') }}
    ),
    niveau_4 AS (
        SELECT
            code,
            libelle
        FROM
            {{ source('collecte_naf', 'naf2008_liste_n4') }}
    ),
    niveau_5 AS (
        SELECT
            code,
            libelle
        FROM
            {{ source('collecte_naf', 'naf2008_liste_n5') }}
    )
SELECT
    niveau_1.code AS code_1,
    niveau_1.libelle AS libelle_1,
    niveau_2.code AS code_2,
    niveau_2.libelle AS libelle_2,
    niveau_3.code AS code_3,
    niveau_3.libelle AS libelle_3,
    niveau_4.code AS code_4,
    niveau_4.libelle AS libelle_4,
    niveau_5.code AS code_5,
    niveau_5.libelle AS libelle_5
FROM
    hierarchie
JOIN
    niveau_1 ON hierarchie.niv1 = niveau_1.code
JOIN
    niveau_2 ON hierarchie.niv2 = niveau_2.code
JOIN
    niveau_3 ON hierarchie.niv3 = niveau_3.code
JOIN
    niveau_4 ON hierarchie.niv4 = niveau_4.code
JOIN
    niveau_5 ON hierarchie.niv5 = niveau_5.code
