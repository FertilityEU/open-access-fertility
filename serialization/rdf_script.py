from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import DCTERMS, PROV, XSD, RDF, RDFS
import os

# Define Namespaces
DCAT = Namespace("https://www.w3.org/ns/dcat#")
ADMS = Namespace("http://www.w3.org/ns/adms#")
FERTILITYEU = Namespace("https://reproduce-for-whom.github.io/OADE_FertilityEurope/")
CC = Namespace("http://creativecommons.org/ns#")

# Create catalog graph
g = Graph()
catalog_g = Graph()
g.bind("dcat3", DCAT)
g.bind("dct", DCTERMS)
g.bind("prov", PROV)
g.bind("adms", ADMS)
g.bind("xsd", XSD)
g.bind("FERTILITYEU", FERTILITYEU)
g.bind("cc", CC)

catalog_g.bind("dcat", DCAT)
catalog_g.bind("dct", DCTERMS)
catalog_g.bind("prov", PROV)
catalog_g.bind("adms", ADMS)
catalog_g.bind("xsd", XSD)
catalog_g.bind("cc", CC)
catalog_g.bind("FERTILITYEU", FERTILITYEU)

#dataset
datasets = [
    {
        "id": "DS1",
        "title": "Total fertility rate by NUTS 2 region",
        "description": "Mean number of children that a woman could have during her childbearing age, by region.",
        "theme": "Population and social conditions ; General and regional statistics",
        "subject": "Fertility",
        "issued": "2025-04-01",
        "publisher": "Eurostat",
        "creator": "Eurostat",
        "rights_holder": "Eurostat",
        "format": ".csv, .tsv, .xlsx, SDMX (.xml, .json)",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "DS2",
        "title": "Population density by NUTS 2 region",
        "description": "Number of inhabitants per km² in each NUTS 2 region.",
        "theme": "Population and social conditions; Regional statistics",
        "subject": "Demographics",
        "issued": "2025-04-02",
        "publisher": "Eurostat",
        "creator": "Eurostat",
        "rights_holder": "Eurostat",
        "format": ".csv, .tsv, .xlsx, SDMX (.xml, .json)",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "DS3",
        "title": "Greenhouse Gas Emissions at sub-national level",
        "description": "EDGAR GHG emission gridmaps supporting territorial climate policy analysis.",
        "theme": "Environment",
        "subject": "Pollution",
        "issued": "2025-04-02",
        "publisher": "EEA",
        "creator": "EEA + EDGAR",
        "rights_holder": "EEA + EDGAR",
        "format": ".csv, .xlsx",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "DS4",
        "title": "Burden of disease of air pollution",
        "description": "Information on burden of disease of air pollution calculated for countries and NUTS regions.",
        "theme": "Environment",
        "subject": "Air Quality",
        "issued": "2025-04-03",
        "publisher": "EEA",
        "creator": "EEA",
        "rights_holder": "EEA",
        "format": ".csv, .tsv, .json, .geojson",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "DS5",
        "title": "Land cover overview by NUTS 2 region",
        "description": "Annual classification of land use patterns by region.",
        "theme": "General and regional statistics ; Cross cutting topics",
        "subject": "Land Use",
        "issued": "2022-07-18",
        "publisher": "Eurostat",
        "creator": "Eurostat",
        "rights_holder": "Eurostat",
        "format": ".csv, .tsv, .xlsx, SDMX (.xml, .json)",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "DS6",
        "title": "Mean and median income by age and sex",
        "description": "Income inequality by NUTS 2 region, measured via GINI coefficient.",
        "theme": "Population and social conditions ; Cross cutting topics",
        "subject": "Income Distribution",
        "issued": "2025-04-30",
        "publisher": "Eurostat",
        "creator": "Eurostat",
        "rights_holder": "Eurostat",
        "format": ".csv, .tsv, .xlsx, SDMX (.xml, .json)",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "DS7",
        "title": "Graduates by education level, programme orientation, sex and field of education",
        "description": "Number of graduates by educational level, age, and region.",
        "theme": "Population and social conditions",
        "subject": "Education",
        "issued": "2025-05-07",
        "publisher": "Eurostat",
        "creator": "Eurostat",
        "rights_holder": "Eurostat",
        "format": ".csv, .tsv, .xlsx, SDMX (.xml, .json)",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "DS8",
        "title": "Expenditure on family/children function by type of benefit and means-testing",
        "description": "Social protection expenditure by function (e.g., health, family, old age). National level.",
        "theme": "Population and social conditions",
        "subject": "Social Expenditure",
        "issued": "2025-04-28",
        "publisher": "Eurostat",
        "creator": "Eurostat",
        "rights_holder": "Eurostat",
        "format": ".csv, .tsv, .xlsx, SDMX (.xml, .json)",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "DS9",
        "title": "Fertility rates by age and NUTS 2 region",
        "description": "Age-specific fertility rates and number of live births per year and region.",
        "theme": "Population and social conditions ; General and regional statistics",
        "subject": "Natality",
        "issued": "2025-04-01",
        "publisher": "Eurostat",
        "creator": "Eurostat",
        "rights_holder": "Eurostat",
        "format": ".csv, .tsv, .xlsx, SDMX (.xml, .json)",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "ms1",
        "title": "Interconnection between Fertility and Environment",
        "description": "Mashup exploring correlation between pollution (emissions, PM₂.₅, NO₂) and fertility. Includes contextual variables.",
        "theme": "Population and society; Environment",
        "subject": "Fertility",
        "issued": "2025-05-05",
        "publisher": "FertilityEU",
        "creator": "Virginia D’Antonio",
        "rights_holder": "FertilityEU",
        "format": ".csv",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "ms2",
        "title": "Interconnection between Fertility and Socioeconomic Conditions",
        "description": "Mashup relating fertility with income, education, and poverty risk. Includes population density as a control.",
        "theme": "Population and society; Economy and finance",
        "subject": "Socioeconomics",
        "issued": "2025-05-05",
        "publisher": "FertilityEU",
        "creator": "Elena Binotti",
        "rights_holder": "FertilityEU",
        "format": ".csv",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "ms3",
        "title": "Interconnection between Regional and National Welfare Mismatch",
        "description": "Mashup comparing fertility and poverty at regional level vs national-level family expenditure.",
        "theme": "Population and society; Government and public sector",
        "subject": "Welfare",
        "issued": "2025-05-05",
        "publisher": "FertilityEU",
        "creator": "Elvira Kushlak",
        "rights_holder": "FertilityEU",
        "format": ".csv",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    },
    {
        "id": "ms4",
        "title": "Interconnection between Regional Clusters and Equity Index",
        "description": "Mashup integrating fertility, pollution, income, and education to rank EU regions by reproductive equity.",
        "theme": "Population and society; Regions and cities",
        "subject": "Equity Index",
        "issued": "2025-05-05",
        "publisher": "FertilityEU",
        "creator": "Elvira Kushlak",
        "rights_holder": "FertilityEU",
        "format": ".csv",
        "license": "https://creativecommons.org/licenses/by/4.0/"
    }
]


# Add to RDF graph
for ds in datasets:
    ds_uri = URIRef(FERTILITYEU[ds["id"]])
    catalog_g.add((URIRef("https://github.com/FertilityEU/open-access-fertility"), DCAT.Dataset, Literal(ds["id"])))
    g.add((ds_uri, RDF.type, DCAT.Dataset))
    g.add((ds_uri, DCAT.title, Literal(ds["title"], lang="en")))
    g.add((ds_uri, DCTERMS.identifier, Literal(ds["id"])))
    g.add((ds_uri, DCTERMS.title, Literal(ds["title"], lang="en")))
    g.add((ds_uri, DCTERMS.description, Literal(ds["description"], lang="en")))
    g.add((ds_uri, DCAT.theme, Literal(ds["theme"], lang="en")))
    g.add((ds_uri, DCTERMS.subject, Literal(ds["subject"], lang="en")))
    g.add((ds_uri, DCTERMS.issued, Literal(ds["issued"], datatype=XSD.date)))
    g.add((ds_uri, DCTERMS.publisher, Literal(ds["publisher"])))
    g.add((ds_uri, DCTERMS.creator, Literal(ds["creator"])))
    g.add((ds_uri, DCTERMS.rightsHolder, Literal(ds["rights_holder"])))
    g.add((ds_uri, DCAT.distribution, Literal(ds["format"])))
    g.add((ds_uri, DCTERMS.language, Literal("en")))
    g.add((ds_uri, DCTERMS.license, URIRef(ds["license"])))



# Define catalog
catalog_uri = URIRef(FERTILITYEU["catalog"])
catalog_g.add((catalog_uri, RDF.type, DCAT.Catalog))
catalog_g.add((catalog_uri, DCTERMS.title, Literal("Generation Zero Project - Datasets Catalog", lang="en")))
catalog_g.add((catalog_uri, DCTERMS.identifier, Literal("GenerationZeroCatalog")))
catalog_g.add((catalog_uri, DCTERMS.description, Literal("This catalog contains datasets about how environment, wealth and welfare shape birth in Europe", lang="en")))
catalog_g.add((catalog_uri, DCTERMS.publisher, Literal("FertilityEU")))
catalog_g.add((catalog_uri, DCTERMS.issued, Literal("2025-05-01", datatype=XSD.date)))
catalog_g.add((catalog_uri, DCTERMS.modified, Literal("2025-05-10", datatype=XSD.date)))
catalog_g.add((catalog_uri, DCTERMS.language, Literal("en")))
catalog_g.add((catalog_uri, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")))
catalog_g.add((catalog_uri, DCTERMS.spatial, Literal("Europe")))
catalog_g.add((catalog_uri, DCTERMS.identifier,  Literal("FertilityEU-Catalog", datatype=XSD.string)))

# License
license_uri = URIRef("https://creativecommons.org/licenses/by/4.0/")
catalog_g.add((catalog_uri, DCTERMS.license, license_uri))

catalog_g.add((license_uri, RDF.type, CC.License))
catalog_g.add((license_uri, CC.legalcode, URIRef("http://creativecommons.org/licenses/by/4.0/")))
catalog_g.add((license_uri, CC.permits, CC.Reproduction))
catalog_g.add((license_uri, CC.permits, CC.Distribution))
catalog_g.add((license_uri, CC.permits, CC.DerivativeWorks))
catalog_g.add((license_uri, CC.requires, CC.Notice))
catalog_g.add((license_uri, CC.requires, CC.Attribution))
catalog_g.add((license_uri, RDFS.label, Literal("Creative Commons CC-BY 4.0", lang="en")))

# Save catalog file
output_dir = "serialization"
os.makedirs(output_dir, exist_ok=True)


#  file in directory
datasets_file = os.path.join(output_dir, "serial_datasets.ttl")
catalog_file = os.path.join(output_dir, "serial_catalog.ttl")

with open(datasets_file, "w", encoding="utf-8") as f:
    f.write(g.serialize(format="turtle"))

with open(catalog_file, "w", encoding="utf-8") as f:
    f.write(catalog_g.serialize(format="turtle"))

print(f"Serializzazione completata! File salvati come {datasets_file} e {catalog_file}.")
