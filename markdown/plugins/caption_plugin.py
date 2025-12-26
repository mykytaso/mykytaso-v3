import re
import mistune


CAPTION_PATTERN = re.compile(
    r':::caption\s*\n(.*?)\n:::',
    re.MULTILINE | re.DOTALL
)

# Create a simple markdown instance for processing inline content
_inline_md = mistune.create_markdown(
    escape=False,
    plugins=['strikethrough', 'url']
)


def preprocess_captions(text):
    """
    Preprocess markdown text to convert :::caption blocks into HTML.
    This is done before mistune processes the markdown to avoid regex conflicts.
    """
    def replace_caption(match):
        caption_text = match.group(1).strip()
        # Process inline markdown (bold, italic, links, etc.)
        # Remove wrapping <p> tags from the processed text
        processed_text = _inline_md(caption_text).strip()
        if processed_text.startswith('<p>') and processed_text.endswith('</p>'):
            processed_text = processed_text[3:-4]
        return f'<p class="caption-text">{processed_text}</p>'

    return CAPTION_PATTERN.sub(replace_caption, text)


def caption_plugin(md):
    """
    Plugin to add caption block support via preprocessing.
    This avoids mistune's regex group naming conflicts.
    """
    # Store the original parse method
    original_parse = md.parse

    # Wrap the parse method to preprocess captions
    def parse_with_captions(text):
        # Preprocess caption blocks before mistune parses
        text = preprocess_captions(text)
        return original_parse(text)

    # Replace the parse method
    md.parse = parse_with_captions
