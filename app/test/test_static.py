import pytest
@pytest.mark.parametrize("path", [
    '/static/fonts/Manrope-Variable.ttf',
    '/static/fonts/Bounded-Variable.ttf'
])

def test_fonts_loadable(client, path): 
    # Path to static font files
    response = client.get(path)
    assert response.status_code == 200      

    # File content should not be empty
    assert len(response.data) > 0

    # Check for valid font file signatures (TrueType or OpenType)
    assert response.data.startswith(b'\x00\x01\x00\x00') or response.data.startswith(b'OTTO')
    # Check for correct MIME type
    assert response.mimetype in {'font/ttf', 'font/otf', 'application/font-sfnt', 'application/octet-stream'}