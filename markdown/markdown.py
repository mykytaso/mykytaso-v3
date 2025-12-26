import mistune

from markdown.plugins.caption_plugin import caption_plugin
from markdown.renderer import CustomRenderer


def markdown_text(text, renderer=CustomRenderer):
    markdown = mistune.create_markdown(
        escape=False,
        hard_wrap=True,
        renderer=renderer(escape=False) if renderer else None,
        plugins=[
            "strikethrough",
            "url",
            "table",
            caption_plugin,
        ]
    )
    return markdown(text)
