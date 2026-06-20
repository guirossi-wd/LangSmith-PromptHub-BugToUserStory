"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
import re
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    @pytest.fixture(scope="class")
    def prompt_data(self):
        """Carrega o prompt otimizado (v2) uma única vez para todos os testes da classe."""
        return load_prompts(PROMPT_PATH)

    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt_data, "Campo 'system_prompt' não encontrado no YAML"

        system_prompt = prompt_data["system_prompt"].strip()
        assert system_prompt, "Campo 'system_prompt' está vazio"

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = prompt_data["system_prompt"]

        has_role = re.search(r"voc[êe]\s+[ée]\s+(um|uma)\b", system_prompt, re.IGNORECASE)
        assert has_role, (
            "Nenhuma definição de persona encontrada. "
            "Esperado algo como 'Você é um(a) ...' no system_prompt."
        )

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data["system_prompt"].lower()

        format_markers = ["markdown", "como um", "eu quero", "para que", "user story"]
        assert any(marker in system_prompt for marker in format_markers), (
            "Nenhuma referência a formato Markdown ou à estrutura de User Story "
            "('Como um... Eu quero... Para que...') foi encontrada no system_prompt."
        )

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data["system_prompt"]

        bug_report_examples = len(re.findall(r"bug report\s*:", system_prompt, re.IGNORECASE))
        user_story_examples = len(re.findall(r"user story\s*:", system_prompt, re.IGNORECASE))

        assert bug_report_examples >= 2 and user_story_examples >= 2, (
            "Esperado pelo menos 2 exemplos de entrada/saída (Few-shot). "
            f"Encontrados {bug_report_examples} ocorrência(s) de 'Bug Report:' e "
            f"{user_story_examples} de 'User Story:'."
        )

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = prompt_data["system_prompt"]

        # Usa o marcador literal "[TODO]" (e não a palavra solta "TODO"),
        # já que palavras comuns em português como "todos"/"método" contêm
        # "TODO" como substring e gerariam falso positivo.
        assert not re.search(r"\[\s*TODO\s*\]", system_prompt, re.IGNORECASE), (
            "O system_prompt ainda contém um marcador '[TODO]' pendente."
        )

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt_data.get("techniques_applied", [])

        assert len(techniques) >= 2, (
            f"Mínimo de 2 técnicas requeridas em 'techniques_applied', "
            f"encontradas: {len(techniques)}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])