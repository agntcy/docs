"""MkDocs hooks to configure SSL certificates for include-markdown plugin."""
import ssl
import certifi

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

