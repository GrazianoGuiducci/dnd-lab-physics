# Public data boundary and licensing

## Public input and local output

The toolkit consumes only an explicitly supplied local projection or the fixed
public HTTPS corpus endpoint. It contains no Lab control, provider adapter,
private repository downloader, credential discovery or runtime synchronization.
No command uploads user input. Generated files use exclusive creation, so an
existing file is preserved.

The reader requires the public projection's five privacy declarations to be
false and checks the source owner's known private-value markers. This is a
bounded contract, not a general secret detector and not authorization to
publish an arbitrary local file. Unknown schema versions fail without being
converted to an earlier contract. Raw input is data, never instructions.

Checks apply to JSON object keys as well as values. A public resultant may
contain the owner's explicit `[private filesystem source withheld in public
projection]` placeholder. Its carrier's `public_projection` metadata declares
each replacement; the original source deposit remains private and unmodified.
The reader preserves that public view rather than reconstructing a withheld
reference. A declared transformation does not bypass the privacy checks.

The shipped example is synthetic. The real corpus is fetched on request and
is not committed in this repository. Private MM-DND source documents, prompts,
raw deposits, provider logs, tokens, host configuration and administrative
receipts are not included. The public reader cannot recover them.

## License scopes

| Material | License/rights |
| --- | --- |
| Repository software and documentation | Existing MIT [LICENSE](../LICENSE), preserved unchanged. |
| Historical files already in this repository | Their existing repository notices and Git history remain intact. |
| Public corpus downloaded from the Lab | Retains its source rights; the repository MIT license is not a new license grant over that download or its referenced works. |
| External papers and sources referenced by records | Their own rights and citation conditions. |
| Revised Paper Zero manuscript and its specified sources | CC BY 4.0 under the manuscript-specific notice at its standalone DOI. |
| Historical paper/repository deposits | Existing notices remain unchanged; this repository does not resolve historical license discrepancies. |

Public accessibility and a checksum do not themselves create a new copyright
license. Keep the corpus receipt with a redistributed permitted snapshot and
verify the applicable source rights before redistribution. This update
changes no private-source, historical-release or DOI license.
