from markdown_it import MarkdownIt

from markdown.renderer import CustomRenderer
from markdown.rules import heading_anchors


# CommonMark, plus the two plugins: table and strikethrough.
markdown = MarkdownIt("commonmark", {"breaks": True}, renderer_cls=CustomRenderer).enable(
    ["table", "strikethrough"],
)

# Give headings an id, but only for markdown headings, not raw HTML.
markdown.core.ruler.push("heading_anchors", heading_anchors)


def markdown_text(text):
    return markdown.render(text)
