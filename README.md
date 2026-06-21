# Mournmore

## About

This project generates **Mournmore Code**, an unofficial Modified Version derived from GitHub’s Monaspace fonts.

The font takes the Argon font family from Monaspace and uses it for the regular font styles and Radon for the italic styles. The name is from the fictional molecule monoradon monoargonide -> moarmorn -> mournmore. I reckon it has a fontish kind of sound to it.

It style-links:

| Mournmore Code style | Source |
|---|---|
| Regular | Monaspace Argon Frozen Regular |
| Italic | Monaspace Radon Frozen Regular |
| Bold | Monaspace Argon Frozen Bold |
| Bold Italic | Monaspace Radon Frozen Bold |

## Usage

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

## Releases

Releases are not automated at this stage. Manual release process:

1. open latest build action artefact
  * go to "Actions"
  * select latest build
  * download its artefact
3. extract TTF files on local machine
4. manually release
  * go to "Releases"
  * click "Draft a new release"
  * create a new tag by incementing the version
  * write any release notes
  * attach the TTF files
  * click "Publish release"

## Licence, copyright &c.

The generated font files are distributed under the SIL Open Font License, Version 1.1.

**Mournmore** is a Reserved Font Name for this project.

The upstream Reserved Font Names — **Monaspace**, **Argon**, **Neon**, **Xenon**, **Radon**, and **Krypton** — are not used as names for the generated font family.

This project is not affiliated with or endorsed by GitHub or the Monaspace authors.

Coded with ChatGPT assistance.
