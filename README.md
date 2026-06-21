# Mournmore

This project generates **Mournmore Code**, an unofficial Modified Version derived from GitHub’s Monaspace fonts.

The font takes the Argon font family from Monaspace and uses it for the regular font styles and Radon for the italic styles. The name is from the fictional molecule monoradon monoargonide -> moarmorn -> mournmore. I reckon it has a fontish kind of sound to it.

It style-links:

| Mournmore Code style | Source |
|---|---|
| Regular | Monaspace Argon Frozen Regular |
| Italic | Monaspace Radon Frozen Regular |
| Bold | Monaspace Argon Frozen Bold |
| Bold Italic | Monaspace Radon Frozen Bold |

The practical purpose is to let editors such as VS Code use Radon for comments by mapping comments to italic.

```json
{
  "editor.fontFamily": "'Mournmore Code', monospace",
  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "scope": ["comment", "punctuation.definition.comment"],
        "settings": {
          "fontStyle": "italic"
        }
      }
    ]
  }
}
```

The generated font files are distributed under the SIL Open Font License, Version 1.1.

**Mournmore** is a Reserved Font Name for this project.

The upstream Reserved Font Names — **Monaspace**, **Argon**, **Neon**, **Xenon**, **Radon**, and **Krypton** — are not used as names for the generated font family.

This project is not affiliated with or endorsed by GitHub or the Monaspace authors.
