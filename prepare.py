import unicodedata
import itertools
import json
from pathlib import Path, PurePath
import re
from typing import Iterator, Tuple, Optional

RE_GITHUB_PATH = re.compile(r".*/unicode/(.*?)\..*")
UCD = Path("ucd_cldr")


def codepoint_or_range(raw) -> Iterator[int]:
    """
    Decode a single hexadecimal codepoint "0020" or an inclusige range "0000..001F"
    """
    r = raw.split("..")
    if len(r) == 1:
        yield int(r[0], base=16)
    else:
        start = int(r[0], base=16)
        end = int(r[1], base=16)
        yield from range(start, end + 1)


def load_emoji_data(base: Path = UCD) -> Iterator[int]:
    """
    Load UCD's emoji-data.txt
    """
    with open(base / "emoji-data.txt", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            codepoint = line.split(";")[0].strip()
            yield from codepoint_or_range(codepoint)


def load_emoji_sequences(
    base: Path = UCD,
) -> Iterator[Tuple[Tuple[int, ...], Optional[str]]]:
    """
    Load UCD's emoji-sequences.txt
    """
    with open(base / "emoji-sequences.txt", encoding="utf-8") as f:
        for line in f:
            line = line.split("#")[0].rstrip()
            if not line:
                continue

            row = line.split(";")
            codepoints = row[0].strip().split()
            all_codepoints = list(
                itertools.product(
                    *(codepoint_or_range(codepoint) for codepoint in codepoints)
                )
            )
            if len(all_codepoints) == 1:
                name = row[2].strip()
                yield (all_codepoints[0], name)
            else:
                yield from ((c, None) for c in all_codepoints)


def load_emoji_zwj_sequences(
    base: Path = UCD,
) -> Iterator[Tuple[Tuple[int, ...], Optional[str]]]:
    """
    Load UCD's emoji-zwj-sequences.txt
    """
    with open(base / "emoji-zwj-sequences.txt", encoding="utf-8") as f:
        for line in f:
            line = line.split("#")[0].rstrip()
            if not line:
                continue

            row = line.split(";")
            codepoints = tuple(int(i, base=16) for i in row[0].strip().split())
            name = row[2].strip()
            yield (codepoints, name)


def load_emoji_variation_sequences(
    base: Path = UCD,
) -> Iterator[Tuple[Tuple[int, ...], Optional[str]]]:
    """
    Load UCD's emoji-variation-sequences.txt
    """
    with open(base / "emoji-variation-sequences.txt", encoding="utf-8") as f:
        for line in f:
            line = line.split("#")[0].rstrip()
            if not line:
                continue

            row = line.split(";")
            codepoints = tuple(int(i, base=16) for i in row[0].strip().split())
            name = row[2].strip()
            yield (codepoints, name)


def load_annotations(
    base: Path = UCD,
) -> Iterator[Tuple[Tuple[int, ...], Optional[str]]]:
    """
    Load CLDR's annotations in JSON
    """
    d = json.load(open(base / "annotations.json", encoding="utf-8"))
    d = d["annotations"]["annotations"]
    for k, v in d.items():
        key = tuple(ord(c) for c in k)
        name = v["tts"][0]
        yield (key, name)


def load_annotations_derived(
    base: Path = UCD,
) -> Iterator[Tuple[Tuple[int, ...], Optional[str]]]:
    """
    Load CLDR's annotations derived in JSON
    """
    d = json.load(open(base / "annotationsDerived.json", encoding="utf-8"))
    d = d["annotationsDerived"]["annotations"]
    for k, v in d.items():
        key = tuple(ord(c) for c in k)
        name = v["tts"][0]
        yield (key, name)


def load_names_list(base: Path = UCD):
    """
    Load UCD's NamesList.txt
    """
    with open(base / "NamesList.txt", encoding="utf-8") as f:
        for line in f:
            if line.startswith(("@", ";", "\t")):
                continue
            hex_code, name = line.split(maxsplit=1)
            code = int(hex_code, base=16)
            name = name.lower()
            yield (code, name)


EMOJI_DATA = set(load_emoji_data())
EMOJI_SEQUENCES = dict(load_emoji_sequences())
EMOJI_ZWJ_SEQUENCES = dict(load_emoji_zwj_sequences())
EMOJI_VARIATION_SEQUENCES = dict(load_emoji_variation_sequences())
ANNOTATIONS = dict(load_annotations())
ANNOTATIONS_DERIVED = dict(load_annotations_derived())
NAMES = dict(load_names_list())


def lookup_name(seq):
    name = ANNOTATIONS_DERIVED.get(seq)
    if name is None:
        name = ANNOTATIONS.get(seq)
    if name is None:
        name = EMOJI_VARIATION_SEQUENCES.get(seq)
    if name is None:
        name = EMOJI_ZWJ_SEQUENCES.get(seq)
    if name is None:
        name = EMOJI_SEQUENCES.get(seq)
    if name is None and len(seq) == 1:
        name = NAMES.get(seq[0])

    if name is None:
        if len(seq) > 1:
            name = "".join(lookup_name((i,)) for i in seq)
        else:
            name = f"unnamed_{seq[0]:04x}"
            print(f"warning: {name}")
    return name


def load_noto_emojis() -> Iterator[Tuple[Tuple[int, ...], Path]]:
    for svg in Path("noto-emoji/svg").glob("emoji_*.svg"):
        seq = tuple(
            int(c, base=16)
            for c in svg.name.removesuffix(".svg").removeprefix("emoji_u").split("_")
        )
        yield (seq, svg)


NOTO_EMOJIS = dict(load_noto_emojis())


def prepare_noto_typst_module():
    noto = {
        "".join(chr(i) for i in seq): str(path.as_posix())
        for seq, path in NOTO_EMOJIS.items()
    }

    with open("noto.json", "w", encoding="utf-8") as f:
        json.dump(noto, f, ensure_ascii=False)

    # prepare emojis to replace
    to_replace = [k for k in noto.keys() if len(k) != 1 or (ord(k),) in EMOJI_SEQUENCES]
    # sort in order to put longer emoji sequence first
    to_replace.sort(key=lambda x: (-len(x), x))

    with open("noto.regex", "w", encoding="utf-8") as f:
        escaped = "|".join(re.escape(k) for k in to_replace)
        f.write(escaped)


def prepare_github():
    github_names = {}
    with open("raw_github.json") as f:
        for k, v in json.load(f).items():
            m = RE_GITHUB_PATH.match(v)
            if m:
                path = m.group(1)
                t = "".join(chr(int(c, base=16)) for c in path.split("-"))
                github_names[k] = t
            else:
                print("ignore non-Unicode Github emoji: ", k)

    sorted_names = sorted(github_names.keys(), key=lambda x: (-len(x), x))
    regex = "|".join(re.escape(name) for name in sorted_names)
    with open("github.regex", "w", encoding="utf-8") as f:
        f.write(":(")
        f.write(regex)
        f.write("):")

    with open("github.json", "w", encoding="utf-8") as f:
        json.dump(github_names, f, ensure_ascii=False)


def main():
    prepare_noto_typst_module()
    prepare_github()


if __name__ == "__main__":
    main()
