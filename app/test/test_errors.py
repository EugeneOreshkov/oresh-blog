def test_404_error(client):
    """Test that 404 error page is displayed for non-existent routes."""
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
    assert b'Page not found.' in response.data

# TEST_500_ERROR PASSED 