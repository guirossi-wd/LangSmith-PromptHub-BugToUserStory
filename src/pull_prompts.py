"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """Pull prompts from LangSmith"""
    try:

        client = Client() #conectar no langsmith
        
        prompt = client.pull_prompt("leonanluppi/bug_to_user_story_v1") #pegar prompt do hub
        #print(prompt)
        prompt_data = {                                      
                  "metadata": prompt.metadata,                     
                  "input_variables": prompt.input_variables,
                  "system_prompt": prompt.messages[0].prompt.template,                                            
                }                                             
        save_yaml(prompt_data, "prompts/bug_to_user_story_v1.yml")
        print("Prompt pulled from LangSmith")
    except Exception as e:
        print(f"Error pulling prompt from LangSmith: {e}")
        return False


def main():
    """Função principal"""
    #verifica se variaveis estão corretas
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False

    #chama função para pull
    pull_prompts_from_langsmith()

if __name__ == "__main__":
    sys.exit(main())
