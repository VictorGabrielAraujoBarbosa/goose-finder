import pytest
from src.analyzer import analyze_files
from src.config import load_exclusion_patterns, should_ignore


class TestIgnoreFilesAndFolders:
    """Testes para funcionalidade de ignorar arquivos e pastas"""

    def test_ignore_files_and_folders(self):
        """Deve ignorar arquivos específicos, pastas e padrões glob"""
        files = [
            'src/main.py',
            'file.txt',
            'ignore_me.txt',
            'test.log',
            'data.tmp',
            'node_modules/package.json',
            '__pycache__/cache.pyc',
            'venv/lib/package.py'
        ]
        exclusions = ['ignore_me.txt', '*.log', '*.tmp', 'node_modules/', '__pycache__/', 'venv/']
        result = analyze_files(files, exclusions)
        assert result == ['src/main.py', 'file.txt']

    def test_no_exclusions_returns_all(self):
        """Sem exclusões, deve retornar todos os arquivos"""
        files = ['file1.py', 'file2.py', 'file3.py']
        result = analyze_files(files, exclusion_patterns=[])
        assert result == files

    def test_default_exclusion_patterns(self):
        """Deve usar padrões padrão quando não especificados"""
        files = ['main.py', 'test.tmp', 'debug.log', '__pycache__/cache.pyc']
        result = analyze_files(files)
        assert 'main.py' in result
        assert 'test.tmp' not in result
        assert 'debug.log' not in result
        assert '__pycache__/cache.pyc' not in result


class TestShouldIgnore:
    """Testes unitários para a função should_ignore"""

    def test_should_ignore_patterns(self):
        """Deve corresponder nomes exatos, prefixos de pasta e padrões glob"""
        patterns = ['test.log', 'node_modules/', '*.pyc', '__pycache__/']
        
        # Exact match
        assert should_ignore('test.log', patterns) is True
        
        # Folder prefix
        assert should_ignore('node_modules/package.json', patterns) is True
        assert should_ignore('__pycache__/cache.pyc', patterns) is True
        
        # Glob pattern
        assert should_ignore('module.pyc', patterns) is True
        
        # Should not ignore
        assert should_ignore('main.py', patterns) is False
        assert should_ignore('src/main.py', patterns) is False


class TestLoadExclusionPatterns:
    """Testes para carregar padrões de exclusão"""

    def test_load_exclusion_patterns(self):
        """Deve retornar lista com padrões comuns de exclusão"""
        patterns = load_exclusion_patterns()
        assert isinstance(patterns, list)
        assert len(patterns) > 0
        assert '__pycache__/' in patterns
        assert 'node_modules/' in patterns
        assert '*.pyc' in patterns