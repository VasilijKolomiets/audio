from googletrans import Translator

translator = Translator()


def translate(origin: str, src='ru', dest='uk'):
    """Wrap the google API.

    Args:
        origin (str): input text string.
        src (str, optional): origin language code. Defaults to 'ru'.
        dest (str, optional): destination language code_description_. Defaults to 'uk'.

    Returns
    -------
       str: translated text.
    """
    result = translator.translate(origin, src=src, dest=dest)
    return result.text
