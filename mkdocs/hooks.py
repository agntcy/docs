"""MkDocs hooks to configure SSL certificates for include-markdown plugin."""
import ssl
import certifi

_STOCK_FENCED_CODE = frozenset(("fenced_code", "markdown.extensions.fenced_code"))


def on_config(config, **kwargs):
    """Drop stock fenced_code; pymdownx.superfences replaces it (see pymdown-extensions docs)."""
    extensions = config.get("markdown_extensions")
    if not extensions:
        return config

    filtered = []
    for item in extensions:
        if isinstance(item, str):
            if item in _STOCK_FENCED_CODE:
                continue
        elif isinstance(item, dict) and len(item) == 1:
            name = next(iter(item.keys()))
            if name in _STOCK_FENCED_CODE:
                continue
        filtered.append(item)

    config["markdown_extensions"] = filtered
    return config


# Monkey patch urllib to use certifi's certificate bundle
def on_startup(**kwargs):
    """Configure SSL context to use certifi certificates."""
    import urllib.request
    
    # Create SSL context with certifi's certificate bundle
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    # Set the default opener to use this context
    https_handler = urllib.request.HTTPSHandler(context=ssl_context)
    opener = urllib.request.build_opener(https_handler)
    urllib.request.install_opener(opener)

