### Fixed
- Paternal and maternal lineages are now distinguishable in the diagrams and charts. Series colours follow a luminance-ordered warm ramp (3.27:1 in greyscale, up from 2.26:1) and carry a non-colour identifier: the maternal branch and node are dashed, the second line series has a dash pattern and its own point marker
- `culture.html`'s food chart had two of three series sharing an identical fill, distinguishable only by border colour
- Chart labels asked for `Lexend`, which no stylesheet ever loaded, so every chart axis and legend silently fell back to the browser default
