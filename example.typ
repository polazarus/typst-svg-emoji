//#import "@local/svg-emoji:0.1.0": setup-emoji, noto, github
#import "./lib.typ": setup-emoji, noto, github

#show: set text(20pt)

#show: setup-emoji.with(font: noto)

= Typst with working emoji! 🎉🎊

== Alignment tests

M😢X🚢M

== Complex emojis

👱‍♀️ `U+1F471 U+200D U+2640 U+FE0F`

⚛️ `U+269B U+FE0F`

== Github naming

```typst #github.at("+1")``` #github.at("+1")

```typst #github.wink``` #github.wink

== Builtin emoji

```typst #emoji.camel``` #emoji.camel

```typst #emoji.rocket``` #emoji.rocket