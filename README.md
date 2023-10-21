# Typst SVG emoji

## Installation guide
You can use this package both locally and in the [Typst online editor](https://typst.app/).

### Local use
To install the package locally, make sure you know how local packages work in Typst. You can take a look [at the documentation](https://github.com/typst/packages#local-packages) if you are not sure.
 - Clone this repository
 - Copy the `github.json`, `github.regex`, `raw_github.json`, `noto.json`, `noto.regex`, `lib.typ`, and `typst.toml` files to `{data-dir}/local/svg-emoji/0.1.0` (you can also copy all of the files from this repository, the ones that are not listed will be reduntant though).
 - You can then import the package to your Typst projects with `#import "@local/svg-emoji:0.1.0": setup-emoji, noto, github` as shown in the example file.

Note: You can copy the package files to a different directory than `local`, for example `my_packages`, but the import will have to reflect it: `#import "@my_packages/svg-emoji:0.1.0" ...`.

### Typst website
 - Clone this repository
 - Copy the `github.json`, `github.regex`, `raw_github.json`, `noto.json`, `noto.regex`, `lib.typ`, and `typst.toml` files to a folder in your project, for example `svg-emoji` (you can also copy all of the files from this repository, the ones that are not listed will be reduntant though and you will be wasting your account storage).
 - You can then import the package with `#import "./svg-emoji/lib.typ": setup-emoji, noto, github`. If you choose a different folder name than `svg-emoji`, make sure it is reflected in the import.