SELECT
    etablissement.version AS version,
    etablissement.codeCommuneEtablissement AS code_commune,
    etablissement.activitePrincipaleEtablissement AS code_activite,
    count(*) AS total
FROM
    {{ source('collecte_sirene', 'sirene_etablissement') }} as etablissement
GROUP BY
    etablissement.version, etablissement.codeCommuneEtablissement, etablissement.activitePrincipaleEtablissement
ORDER BY
    etablissement.codeCommuneEtablissement, etablissement.activitePrincipaleEtablissement