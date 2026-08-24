from slugify import slugify


def heading_text(inline_token):
    """
    The plain text of a heading, for its anchor.

    `code_inline` is included on purpose: markdown-it keeps the text of a `code span` on the token itself,
    not in a child text token, and `renderInlineAsText` drops it.
    A heading such as "The `save()` method" would otherwise lose half its words.
    """
    return "".join(
        child.content
        for child in inline_token.children or []
        if child.type in {"text", "code_inline"}
    )


def heading_anchors(state):
    """
    Core rule: give every markdown heading a unique id, so a section can be linked to.

    It runs at the end of the core chain, after `text_join`, so the children of
    an inline token are already merged and `heading_text` sees whole words.

    Two headings with the same text would give the same slug, and an id must be unique on a page.
    The second one gets a "-1" suffix, the third "-2".

    Only markdown headings are reached. A heading written as raw HTML (`<h3 align="center">…</h3>`) parses into an `html_block` token,
    not a `heading_open`, so it keeps whatever id its author typed — none by default.
    """
    used_slugs = {}

    for index, token in enumerate(state.tokens):
        if token.type != "heading_open":
            continue

        slug = slugify(heading_text(state.tokens[index + 1])) or "section"
        used_slugs[slug] = used_slugs.get(slug, 0) + 1
        if used_slugs[slug] > 1:
            slug = f"{slug}-{used_slugs[slug] - 1}"

        token.attrSet("id", slug)
