import mistune


def markdown_text(text):
    markdown = mistune.create_markdown(
        escape=False,
        hard_wrap=True,
        # renderer=renderer(escape=False) if renderer else None,
        plugins=[
            "strikethrough",
            "url",
            "table",
            "speedup"
        ]
    )
    return markdown(text)

