# Column Notes — Sources

Sources used to research `column-notes.json`, per collection. Column names were
verified against the catalog parquet files with DuckDB (`DESCRIBE SELECT * FROM
'catalog/<topic>/<id>/<id>.parquet'`) on 2026-08-05 (post-restructure topic
paths). Descriptions marked "(name-based)" or "(inferred)" in the JSON could not
be matched to an official definition and are labeled as such there.

## Key official sources (used across the assessor/permit collections)

- **City of St. Louis controlled vocabularies** (official code tables on the
  open-data portal, index at <https://www.stlouis-mo.gov/data/vocabularies/>;
  CSV per vocabulary at
  `https://www.stlouis-mo.gov/customcf/endpoints/metadata/vocabulary-elements-download.cfm?id=N&format=csv`):
  - id=1 Neighborhood, id=13 Permit Application Type, id=14 Permit Project
    Type, id=16 Permit Structure Type, id=17 Permit Use Group, id=21 Address
    Type, id=22 Assessment Appeal Type, id=23 Assessor Class Code,
    **id=24 Assessor Land Use** (the 922-code table that decodes
    AsrLandUse1/AsrLanduse2/LANDUSE1-4: 1110 = SINGLE FAMILY UNITS, 1010 =
    VACANT RESIDENTIAL LOT, 1120 = TWO FAMILY UNIT, 5000 = TRADE, 1140 = FOUR
    FAMILY UNIT, 3000 = INDUSTRIAL, …), id=41 Parcel Sub Type, id=50 Sale
    Type, id=53 Zoning Code, id=64 Property Class Code, id=70 Abatement Type,
    id=92 Flood Plain Type, id=96 Number Of Units Source.
- **City per-distribution field definitions** (official, at
  `https://www.stlouis-mo.gov/customcf/endpoints/metadata/fields-download.cfm?distributionID=N&format=csv`):
  - distributionID=189 — "2017–2023 Parcels" field definitions (used for
    parcels-history: ASMT*, ASRCLASS*, LANDUSE* → vocabulary 24, VACANTLAND,
    OWNER*, BDG1*, DAILY*/BOOK* labels).
  - distributionID=195 — "Parcel Joining Data" field definitions (used for
    parcels/property-taxes: HANDLE "originally introduced to aid in the
    handling of condominiums … DEPRECATED", ParcelId = Assessor's 2021 schema,
    ColParcelId/ColCityBlock/ColParcel = Collector of Revenue scheme,
    Low/HighAddrNum, SITEADDR, AddrType→vocab 21, AsrClassCode→23,
    AsrLandUse→24).
  - distributionID=2 — CSB Service Requests field definitions (all 311
    descriptions, incl. PROBADDTYPE "A = Parcel, B = Intersection" and
    SUBMITTO).
  - distributionID=231 — Animal Bites; distributionID=235 — Siren Locations.
- **City parcel code databases** (official lookup DBs published by the city):
  - `https://www.stlouis-mo.gov/data/upload/data-files/codes.zip` →
    `PrclCode.mdb` tables **CdOwnerOccCode** (OWNEROCC: 1 Single Family, 2
    2-Family, 4 3-or-4 Family, 5 5+ Family, C Condo, X Other), **CdOwnerCode**
    (0 Standard … 9 Demo/Maintenance Charge), **CdSpecParcelType**,
    **CdSubParcelType**; `corcode.mdb` **CdNLCType** (NLC street-code types);
    `ComCode.mdb` **CdPrclErr** (PRCLERR geocode match codes).
  - `https://www.stlouis-mo.gov/data/upload/data-files/prcl.zip` → `prcl.mdb`
    (the Property Taxes Access DB; its portal page documents "key fields:
    CITYBLOCK, PARCEL, OWNERCODE"), incl. `CdAttrTypeNum` district lookups.
- Missouri assessed-value percentages (19% res / 32% comm / 12% agr): RSMo
  § 137.115 (cited for the Asd* vs Apr* relationship).
- Legacy ID construction notes (Parcel9 = BBBBbbPPP, Parcel10/11 = +OwnerCode,
  HANDLE composition): third-party but city-derived legacy mapping workbook
  summarized in `jonathanleek/civic-data-warehouse`
  (`documentation/data_dictionary/legacy_workbook_useful_findings.md`) — used
  only for the Parcel9/PARCEL10 schema notes and flagged accordingly.
- LANDAREA/SQFT units verified empirically: values match the parcel polygon
  area computed in the foot-based state-plane geometry (`SHAPE.STArea()`).

## Per collection

### parcels, property-taxes, parcels-history, tax-abated-parcels, city-blocks
City controlled vocabularies (1, 21, 22, 23, 24, 41, 50, 53, 64, 70, 92, 96);
field-definition CSVs for distributions 189 and 195; PrclCode.mdb /
corcode.mdb / ComCode.mdb code tables from codes.zip; prcl.zip portal page
(dataset id=3, distribution id=6); RSMo 137.115. `era` (parcels-history) is
documented from this repo's own build (merged yearly snapshot extracts,
`stl_parcels_1997-2000.zip` etc. per the collection AGENTS.md). Not found:
official decode for CDALandUse1/2, RedevPhase phases, and formal documentation
of the Asd* vs Bill* distinction — all noted as such in the JSON.

### lead-service-lines
`staging/extracts/lead-service-lines/layer-metadata.json` — ArcGIS coded-value
domains for all six code fields (material, source, status on both sides), with
aliases "Right of Way …" (utility side) and "Building Side …" (customer side).
Status categories (Unknown / Lead / Non-Lead / Galvanized Requiring
Replacement) and the material-determination "source" concept follow EPA's Lead
and Copper Rule Revisions (LCRR) service line inventory requirements
(<https://www.epa.gov/dwreginfo/lead-service-line-inventory>).

### crime
FBI NIBRS documentation for offense codes/categories and the Crimes Against
(Person/Property/Society) classification
(<https://www.fbi.gov/how-we-can-help-you/more-fbi-services-and-information/ucr/nibrs>),
and the legacy SRS/UCR Part I offense classes (01 homicide … 07 motor vehicle
theft) with its hierarchy rule for IncidentTopSRS_UCR. Code-to-category
mappings were cross-checked against the data itself (09A Murder, 13A Agg
Assault, 23G Theft of MV Parts, 240 MVT, 290 Vandalism all consistent).
VictimNum semantics (an identifier, not a count) verified empirically.
FelMisdCit decode (values F/M/C/I) is not published by SLMPD — noted as
partially inferred. SLMPD's site (slmpd.org, source of the download per the
portal dataset id=69) is behind bot protection and could not be fetched.
`keep` documented from this repo's `tools/assemble.py`.

### electrical/mechanical/plumbing/occupancy-permits
City controlled vocabularies id=13 (Permit Application Type: AE/AM/AP/AO
match each dataset's observed APPTYPE), id=14 (Permit Project Type), id=16
(Permit Structure Type), id=17 (Permit Use Group, for the occupancy
NEW/OLDUSEGROUP fields); ComCode.mdb CdPrclErr for PRCLERR. CANCELTYPE has no
published decode (only 'C' observed) — noted.

### vacancy-composite
Source layer name `SLDC.SLDC.Tol_Def_Vac_NP` (AGOL item
98a6f429617546be9d9b467c5ad1dafc, no description published) identifies the
SLDC/Tolemi (BuildingBlocks) "definite vacancy" composite. Field names are
shapefile-truncated and no public data dictionary was found (stlvacancy.com
methodology pages contain no field-level docs); descriptions are conservative
name-based expansions and are flagged. Not found: decodes for TOLEMI_DEF,
LRA_RORE, NSR_OWNED_, BISA_SCORE, PROPERTY_T, OWNER_TENU.

### market-value-analysis
Official field-by-field documentation in the ArcGIS Online item description
for "2024 Market Value Analysis"
(<https://stlcity.maps.arcgis.com/home/item.html?id=e71e3ebca1f345a4b7db134d30c5d9ff>),
including sources per indicator (City of St. Louis administrative data, ACS
2018-2022, NHPD/HUD-POSH/SLHA) and the Reinvestment Fund cluster-analysis
methodology summary. Two documented names differ from the actual columns
(CHOO→CHHOO, CHIH→CHH) — noted in the JSON.

### land-use
Category code names from the City's adopted 2005 Strategic Land Use Plan PDF
(<https://www.stlouis-mo.gov/government/departments/planning/planning/adopted-plans/strategic-land-use/documents/upload/SLUP_2005.pdf>),
which spells out NPA, NDA, NCA, RCA, BIPA, BIDA, IPDA, ROSPDA, SMUA, OA.
Values verified against SLUP_LATES in the parquet. Other fields are
name-based (flagged). Note: the city adopted a new 2025 SLUP with different
categories; this dataset still carries the 2005-scheme codes.

### zoning
District names verbatim from the city's ArcGIS renderer labels, as captured in
this repo's `tools/make_styles.py` ZONE_NAMES (A–L), consistent with the city
'Zoning Code' controlled vocabulary (id=53).

### csb-311-requests
Official field definitions CSV for distribution id=2 of dataset id=5 (CSB
Service Requests). PARENT_/GRANDPARENT_ hierarchy fields, PUBLICRESOLUTION and
PROBLEMSID are not in the official list — flagged as name-based. `keep` from
`tools/assemble.py`.

### election-results-nov-2024, election-precincts, polling-places
No portal field definitions found; descriptions are from the canvass-file
column names plus standard U.S. election tabulation terminology (overvote /
undervote, e.g. the EAC glossary) — flagged accordingly.

### animal-bites
Official field definition CSV (distribution 231).

### siren-locations
The parquet is a field-inspection ArcGIS layer whose columns differ from the
portal's siren spreadsheet; only 'Siren' and 'SIREN_LOCATION_ADDRESS' map to
the official distribution-235 labels — the inspection fields (conditions,
pole, test dates) are name-based and flagged.

### property-sales
City controlled vocabulary id=50 'Sale Type' for SaleType; other fields
name-based against the parcel-key documentation.

### lra-property
Portal dataset id=30 field CSVs (distributions 144-147, 229 — LRA offer
records: RECORD_NO definition) plus the LRA program context from the city's
Land Reutilization Authority pages; Proposition NS program context from the
city's Prop NS pages. Most fields name-based — flagged.

## Overture collections (`overture-column-notes.json`)

The 10 `overture-*` collections are not city data, so their glosses come from
Overture's own documentation rather than the portal:

- **The Overture schema itself** — the authoritative per-property text, read
  from <https://github.com/OvertureMaps/schema> (`schema/defs.yaml` for the
  properties shared by every theme: `id`/GERS, `sources`, `names`, `level`,
  `version`, `wikidata`, `cartography`; `schema/base/defs.yaml` for
  `source_tags`, `surface`, `elevation`; then `schema/<theme>/*.yaml` per
  feature type). Enum members quoted in the glosses are that file's `enum`
  lists. Read from the repository's `main` branch, which can run ahead of the
  pinned `OVERTURE_RELEASE` — which is why no gloss states an exact count of
  enum members, only the shape of the list and representative values.
- **The theme guides** at <https://docs.overturemaps.org/guides/> (base,
  places, addresses) and <https://docs.overturemaps.org/gers/> for the
  framing sentences: land cover derived from ESA WorldCover, land cover
  versus land use, the places definition and its licensing, the addresses
  theme aggregating 175-plus independently licensed sources, GERS IDs being
  stable across releases.
- **Not in either**: `overture_type`, `building_id` on merged rows, `bbox`,
  and the clipping note on every `geometry` describe what *this mirror* did
  during extraction (`tools/fetch_overture.py`, gpio conversion), not
  Overture's schema, and each gloss says so.
- Column names were verified against the catalog parquet files, and the
  claims that are about this extract rather than the schema were checked with
  DuckDB against the published files: subtype null on every connector row,
  `region` being US-MO/US-IL, every `building_part` row joining to a building
  on `building_id`, and the land theme's points being overwhelmingly single
  trees.

## What could not be found (summary)

- Official decode tables for: CDALandUse1/2, RedevPhase, CANCELTYPE,
  FelMisdCit (beyond F/M), OWNERGROUP, and all Tolemi vacancy-composite coded
  fields (TOLEMI_DEF, LRA_RORE, NSR_OWNED_, BISA_SCORE, PROPERTY_T,
  OWNER_TENU).
- Formal documentation of the Asd*/Bill*/Apr* three-way distinction (described
  from structure + RSMo assessment law only).
- An expansion of the "NLC" acronym (the street-code type table exists in
  corcode.mdb but no document expands the name).
- SLMPD's own crime-file data dictionary (site blocks automated access).
- Field-level documentation for the elections canvass export.
