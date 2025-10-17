def test_font_loadable(client):
    """Test if the font file is accessible."""
    font_path = '/app/static/fonts/Manpore-Variable.ttf'
    response = client.get(font_path)
    assert response.status_code == 200
    assert response.mimetype == 'font/ttf'
    assert len(response.data) > 0
    assert response.data.startswith(b'\x00\x01\x00\x00')  # TrueType font file signature
    assert b'Manpore-Variable' in response.data  # Check if the font name is in the file content
