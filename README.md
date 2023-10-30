# Typst SVG emoji

A hopefully temporary Typst package to work around spotty support of color Emoji.

Basic idea: replace automically every emoji use by the corresponding SVG image from a font (for now, only [Noto](https://github.com/googlefonts/noto-emoji).

## Installation and usage

_thx [Pandicon](https://github.com/Pandicon)_

You can use this package both locally and in the [Typst online editor](https://typst.app/).

### Local use

To install the package locally, make sure you know how local packages work in Typst.
Please take a look [at the documentation](https://github.com/typst/packages#local-packages) if you are not sure.

- Clone this repository to `{data-dir}/local/svg-emoji/0.1.0`
- Import `@local/svg-emoji:0.1.0` in your Typst project, for example:
 


```typst
#import "@local/svg-emoji:0.1.0": setup-emoji, github // only if you want to use GH names for emojis

// first install the emoji hook!
#show: setup-emoji

// directly
😆🛖🐡

// builtin emoji namespace
#emoji.rocket

// or use github-named emojis
#github.blue_car
```

Note: You can copy the package files to a different directory than `local`, for example `my_packages`, but the import will have to reflect it: `#import "@my_packages/svg-emoji:0.1.0" ...`.

### Typst.app website

- Clone this repository
- Copy the `github.json`, `raw_github.json`, `noto.json`, `noto.regex`, `lib.typ`, `noto-emoji/svg/*` files (keeping the directory structure)  to a directory in your project, say `svg-emoji`
- Import the lib file in your Typst project

  ```typst
  #import "./svg-emoji/lib.typ": setup-emoji, github

  // see above for usage
  ```
  
  If you choose a different folder name than `svg-emoji`, make sure it is reflected in the `#import`.

## TODO

- more doc
- prepare release in CI
- understand why `setup-github` does not currently work