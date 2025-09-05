from terraform_champ.file_utils import get_excluded_directories

def test_get_excluded_directories(monkeypatch):
    expected = set()
    assert get_excluded_directories() == expected
    
    monkeypatch.setenv("TFCHAMP_EXCLUDED_DIRS", "foo,bar")
    expected = {"foo", "bar"}
    assert get_excluded_directories() == expected
    
    monkeypatch.setenv("TFCHAMP_EXCLUDED_DIRS", "  foo,   bar   ")
    expected = {"foo", "bar"}
    assert get_excluded_directories() == expected