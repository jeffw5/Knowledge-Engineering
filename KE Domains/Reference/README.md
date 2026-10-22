# Reference

`apqc-pcf/`: the APQC Process Classification Framework reference registry, the APQC PCF Taxonomy 0.2.0 at `…/taxonomy/apqc-pcf/` (D25, D29). It is read only, built by `../_build/build_reference.py`.

- **Source.** APQC Cross-Industry PCF **7.4** (August 2024), categories 3.0 Market and Sell Products and Services and 6.0 Manage Customer Service (309 elements). `apqc-pcf/source/` holds the source text and the links to APQC's PDF and Excel. The PCF is APQC's open standard and is used here with attribution.
- **Newer release.** APQC released PCF 8.0 on 2026-02-27. Save a copy in `apqc-pcf/source/` and the registry moves to it (open question 29).
- **What each element records.** An element (`…/apqc-pcf/element-<APQC ID>`) keeps:
  - APQC's name, as published;
  - its hierarchy number (`skos:notation`);
  - its element ID (`dcterms:identifier`);
  - its level (category, process group, process, activity, task);
  - its one owner domain (`skos:related` to the domain concept in the owner's area taxonomy);
  - whether a PEO performs it (`skos:note "PEO applicability: Applicable | Adapted. … | Not applicable. …"`).
- **How domains use it.**
  - The Commercial Operations activities and steps are classified by the element they are or extend (`dcterms:type`, D28).
  - The topology on Service Assembly shows the process groups (L2) and processes (L3) from the registry.
  - Older domain process kinds link to it with `skos:exactMatch` or `skos:broadMatch`.
  - No domain re-creates an APQC element.
- **Crosswalk.** `apqc-pcf/crosswalk-7.2.1-to-7.4.csv` maps the previous release by element ID: added, removed, renumbered, renamed, unchanged.
- **What it doesn't cover.** External services follow the business model, not APQC.
