import mistune
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer


class CustomRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        """
        Pygments processes text in three steps: lexing, filtering, and formatting.

        A lexer converts source text into semantic tokens (keywords, strings, comments).
        Optional filters can modify these tokens or their content.
        A formatter outputs the tokens in formats like HTML or LaTeX, while a style
        defines how each token type is visually highlighted.
        """

        # Determine the lexer based on the info string (language)
        if info:
            try:
                lexer = get_lexer_by_name(info, stripall=True)
            except Exception:
                lexer = TextLexer()
        else:
            lexer = TextLexer()

        # Configure the HTML formatter with desired style and options
        formatter = HtmlFormatter(
            cssclass="highlight",
            style="dracula",  # nord-darker, monokai, material, dracula, lightbulb, one-dark
            noclasses=True,   # Use CSS classes instead of inline styles
        )

        return highlight(code, lexer, formatter)


    def image(self, alt, url, title=None):
        escaped_alt = mistune.escape(alt) or ""
        escaped_url = mistune.escape(url)

        image_size = ""
        if title:
            escaped_title = mistune.escape(title)
            image_size = f'class="img-{escaped_title}"'

        image_tag = f'<img src="{escaped_url}" alt="{escaped_alt}" {image_size}>'
        caption = f"<figcaption>{escaped_alt}</figcaption>" if escaped_alt else ""
        return f"<figure>{image_tag}{caption}</figure>"
