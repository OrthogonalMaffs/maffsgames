# Vendored specification sources

Source documents are vendored here so that the derived data in `data/spec-mapping.json`
can be re-derived and audited rather than trusted. Each file's SHA256 is asserted by the
script that reads it and recorded in the data file's `sources` block.

Do not edit these files. Replace them only with a newer published version, and when you do,
update the SHA256 in the extractor and re-run it — the hash assertion exists so that a
silently swapped source fails loudly instead of quietly changing the tier data.

## dfe-gcse-maths-subject-content.pdf

- **Title:** Mathematics: GCSE subject content and assessment objectives
- **Publisher:** Department for Education
- **URL:** https://assets.publishing.service.gov.uk/media/5a7cb5b040f0b6629523b52c/GCSE_mathematics_subject_content_and_assessment_objectives.pdf
- **SHA256:** `647a751b51c71d9ced1c9356aa70b15ceb1a4acb2fd5bc9af49619ead06d0ee6`
- **Retrieved:** 24 September 2026
- **Read by:** `scripts/extract-dfe-tier.py`

### Licence

© Crown copyright 2013. Contains public sector information licensed under the
[Open Government Licence v3.0](http://www.nationalarchives.gov.uk/doc/open-government-licence/).

The document's own licence line permits re-use "in any format or medium", which is what
allows it to be vendored here. **The OGL excludes logos.** This PDF contains the
Department for Education logo on its cover: redistributing the document as published is
fine, but that logo must never be lifted out and used on the site or in any MaffsGames
material, because doing so would imply departmental endorsement. This repository is public,
so that carve-out is worth keeping in view.

Third-party copyright material, if any is identified in the document, is likewise not
covered by the OGL.

### Status at time of retrieval

The current GCSE mathematics specifications built on this content are live, not withdrawn.
Curriculum reform is at first teaching 2029/2030 with the final curriculum published spring
2027, so this document remains the operative subject content. Separately, DfE has confirmed
that students will not be expected to memorise formulae for the remaining lifetime of the
current specifications, and formulae sheets will continue to be provided.
