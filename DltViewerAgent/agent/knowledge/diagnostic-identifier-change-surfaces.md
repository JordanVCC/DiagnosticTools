# Diagnostic Identifier Change Surfaces

## Scope

Places where DID, RID, or DTC changes can affect diagnostic behavior, decoding,
availability, or product-to-product consistency. Use this page when a case suggests that
a diagnostic identifier exists in one release, product, cluster, or tool but behaves
differently elsewhere.

The values below are project knowledge from the Confluence page `Adding DID/RID/DTC`.
DID and RID are described as following the same workflow. The DTC workflow was marked in
the source as not fully exercised and based on what had been communicated so far.

## Change Surfaces

| Surface | What can change | Behavior impact to consider |
| --- | --- | --- |
| CARCOM / GMRDB SPA Draft | ID reservation, identifier group, description, comments, parameter definitions, units, offsets, bit lengths, and compare values. | Identifier metadata or parameter layout can differ from the intended manifest. Incorrect offsets, bit lengths, units, or compare-value formatting can change decoding or validation behavior. |
| GMRDB approval | Whether the base DID, RID, or DTC is approved for use across future projects. | Approval reserves the ID. After approval, later DID changes may not require GMRDB updates, so CARCOM metadata may not be the freshness authority for behavior. |
| Zenseact manifest | The YAML manifest that defines the diagnostic content to be integrated. | Manifest content can be newer or more authoritative than CARCOM metadata for implemented behavior. Keep the manifest for traceability when available. |
| Manifest checker | Unit and manifest validation before submission. | Unit errors or invalid manifest content can block or delay integration. New units should be avoided unless really needed because unit approval is a separate source of friction. |
| Diagnostics repository import | Import of the checked manifest into the diagnostics repository, usually through a VIRA/Jira flow handled by Team Espresso. | Behavior may depend on whether the diagnostics repository has received the manifest and which products the merge reached. |
| Product sync files | Generated sync output per product or platform baseline from ConfigHub. | Latest sync files can show which identifiers are present for a specific product. Product-specific sync files can explain why an identifier is available or decoded in one product but not another. |
| Application implementation | Camera or diagnostics application support for a DID, RID, or DTC. | A DTC can be implemented and function before CARCOM knows how to decode it. In that state, behavior can be normal except that CARCOM reports missing interpretation data. |
| CARCOM DTC import timing | Manual import of DTCs into CARCOM per release. | DTCs may appear in CARCOM late, sometimes near release, even after application-side and Zenseact-side work is complete. Missing CARCOM decoding does not by itself prove the DTC is not implemented. |
| FTB / DTC last-byte selection | The last two hex digits of the DTC code. | FTB values cannot be selected arbitrarily; they must align with SAE J2012 and ISO 15031-6. Invalid FTB selection can produce incorrect or non-standard DTC meaning. |

## Product Sync Files

Latest sync files can be viewed from ConfigHub by opening a recent baseline such as
`spa2_int` or `Spa3_int`, selecting `HPAA`, opening the linked configuration, and
downloading the `tgz` package.

Known sync-file purposes from the source page:

| Sync file | Product / platform |
| --- | --- |
| `GMRDB_sync_config_hpagen3_ad` | SPA2 config 1/2 HPA |
| `GMRDB_sync_config_hpagen3_adas` | SPA2 HPA; effectively the same as `hpagen3_ad` in the source note |
| `GMRDB_sync_config_hpagen4` | SPA3 config 1 HPA |
| `GMRDB_sync_config_hpagen4_high` | SPA3 config 1.5 HPA |
| `GMRDB_sync_config_hpb` | SPA2 config 2 HPB |

## Reporting Guidance

- When a DID, RID, or DTC behaves differently between releases or products, identify
  which surface is being checked: CARCOM/GMRDB, Zenseact manifest, diagnostics repository
  import, product sync file, application implementation, or CARCOM decoding/import.
- Distinguish implementation from decoding. If CARCOM says `Data for interpretation in
  carcom is missing`, report that the DTC may still be implemented and operating, but the
  CARCOM interpretation data is absent or not yet imported.
- For DID/RID issues, check parameter layout details: offset bits, number of bits, units,
  compare values, and naming/description metadata.
- For DTC issues, check whether the base DTC was approved, whether the implementation and
  manifest exist, whether the diagnostics repository import landed for the relevant
  products, and whether the FTB value follows SAE J2012 / ISO 15031-6.
- Use product sync files to confirm product-specific availability before concluding that
  a diagnostic identifier is globally missing.

## Caveats

- The DTC process in the source page was not fully confirmed by direct execution. Treat
  DTC lifecycle details here as project knowledge with lower confidence than the DID/RID
  workflow.
- CARCOM metadata, product sync files, manifests, and application implementation can be
  temporarily out of sync. Do not treat any single surface as complete proof without
  checking the behavior question being asked.
- This page explains diagnostic identifier change surfaces. It does not list diagnostic
  DID availability or DTC suffix mappings; use `diagnostics.md` for those values.