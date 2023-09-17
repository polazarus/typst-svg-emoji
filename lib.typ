#let noto = (
    dict: json("noto.json"),
    regex: read("noto.regex"),
)

#let github = json("./github.json")

#let emoji-image(svg, alt: "", height: 1em) = {
    style(styles => {
        let h = measure([X], styles).height
        box(
            align(horizon, image(svg, format: "svg", height: height, alt: alt)),
            height: h,
            outset: (y: (height - h) / 2),
        )
    })
}

#let setup-emoji(font: noto, height: 1em, body) = {
    show regex(noto.regex): it => {
        emoji-image(
            alt: it.text,
            height: height,
            noto.dict.at(it.text)
        )
    }
    [with svg emoji font]
    body
}

// do not work
#let setup-github(body) = {
    let re = read("github.regex")
    let data = json("./github.json")
    show regex(re): it => {
        let t = it.text
        let n = t.len()
        data.at(t.slice(1, n - 1))
    }
    [with github]
    body
}
