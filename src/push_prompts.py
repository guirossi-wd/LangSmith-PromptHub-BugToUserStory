"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    client = Client()

    prompt_template = ChatPromptTemplate.from_template(prompt_data["system_prompt"])

    url = client.push_prompt(
        prompt_name,
        object=prompt_template,
        tags=[
            f"{prompt_data['version']}"
        ],
        description=prompt_data["description"])
    print(f"\n\nPrompt pushed to LangSmith Hub: \n{url}\n\n")
    if url == None:
        return False
    return True

def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    is_valid, errors = validate_prompt_structure(prompt_data)
    return (is_valid, errors)


def main():
    """Função principal"""
    #verifica se variaveis estão corretas
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False


    is_valid, errors = validate_prompt(load_yaml("prompts/bug_to_user_story_v2.yml"))
    if not is_valid:
        print("Prompt inválido\nErros: ", errors)
        return False

    #chama função para push
    if not push_prompt_to_langsmith("bug_to_user_story_v2", load_yaml("prompts/bug_to_user_story_v2.yml")):
        print("Erro ao fazer push do prompt")
        return False


if __name__ == "__main__":
    sys.exit(main())
