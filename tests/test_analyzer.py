import pytest
from src.analyzer import analyse_repository


class TestAnalyseRepository:

    def test_REPO01_non_git_directory_raises_value_error(self, tmp_path):
        """REPO-01: Passing a directory without a .git folder should raise ValueError."""
        with pytest.raises(ValueError, match="not a valid Git repository"):
            analyse_repository(str(tmp_path))
