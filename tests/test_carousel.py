def test_carousel_changes(home_page):
    # Verify that the carousel is changing
    is_changing = home_page.is_carousel_changing()
    assert is_changing is True, "The carousel did not change as expected"