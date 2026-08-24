from markdown_it.common.utils import escapeHtml, unescapeAll
from markdown_it.renderer import RendererHTML
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound


class CustomRenderer(RendererHTML):
    """
    A markdown-it renderer with Pygments code blocks and figure-wrapped images.

    RendererHTML collects its rules from its own methods, keeping every method whose name does not start with "render" or "_".
    A method named after a token type replaces the default rule for that token, and a helper with a leading underscore stays out of the rule table.
    """

    def _highlight_code(self, code, info):
        """
        Pygments processes text in three steps: lexing, filtering, and formatting.

        A lexer converts source text into semantic tokens (keywords, strings, comments).
        Optional filters can modify these tokens or their content.
        A formatter outputs the tokens in formats like HTML or LaTeX, while a style defines how each token type is visually highlighted.
        """

        # Determine the lexer based on the info string (language)
        if info:
            try:
                lexer = get_lexer_by_name(info, stripall=True)
            except ClassNotFound:
                lexer = TextLexer()
        else:
            lexer = TextLexer()

        # Configure the HTML formatter with desired style and options
        formatter = HtmlFormatter(
            cssclass="highlight",
            style="dracula",  # nord-darker, monokai, material, dracula, lightbulb, one-dark
            noclasses=True,   # Write the colours as inline styles, not as CSS classes
        )

        return highlight(code, lexer, formatter)

    def fence(self, tokens, idx, options, env):
        """
        A fenced code block. Its info string holds the language name.

        The `highlight` option of markdown-it cannot do this work:
        markdown-it keeps the output of that callback only when it starts with `<pre`, and Pygments starts with `<div class="highlight">`.
        Through the option the block would get a second `<pre><code>` around it.
        """
        token = tokens[idx]
        info = unescapeAll(token.info).strip().split(maxsplit=1)
        return self._highlight_code(token.content, info[0] if info else "")

    def code_block(self, tokens, idx, options, env):
        """An indented code block. It carries no language."""
        return self._highlight_code(tokens[idx].content, "")

    def image(self, tokens, idx, options, env):
        token = tokens[idx]
        escaped_alt = escapeHtml(self.renderInlineAsText(token.children or [], options, env))
        escaped_url = escapeHtml(token.attrGet("src") or "")

        image_size = ""
        title = token.attrGet("title")
        if title:
            escaped_title = escapeHtml(title)
            image_size = f'class="img-{escaped_title}"'

        image_tag = f'<img src="{escaped_url}" alt="{escaped_alt}" {image_size}>'
        caption = f"<figcaption>{escaped_alt}</figcaption>" if escaped_alt else ""
        return f"<figure>{image_tag}{caption}</figure>"
