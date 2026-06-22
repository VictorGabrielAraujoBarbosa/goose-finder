"""Helper compartilhado entre os arquivos de teste."""
from unittest.mock import MagicMock


def arquivo_mock(filename="foo.py", source_code="x = 1", source_code_before="x = 0"):
    """Cria um mock de ModifiedFile do PyDriller."""
    arq = MagicMock()
    arq.filename = filename
    arq.source_code = source_code
    arq.source_code_before = source_code_before
    return arq
