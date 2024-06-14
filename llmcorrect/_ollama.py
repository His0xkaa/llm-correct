"""
llmcorrect._ollama  - ollama wrapper
"""
__all__ = [
    'llmcorrect_ollama_correct',
]
from typing import Any, cast

import ollama
import httpx

from llmcorrect.exception import LlmcorrectException

#---
# Internal
#---

__PROMPT_OLLAMA = """
Tu es un correcteur de texte, peux-tu corriger le texte suivant s'il te
plaît retourne le texte corrige sans m'expliquer. Tu respecteras les 4
regles suivantes:
- Regle 1 : Ne rajoute aucune description qui montre que tu as corrigé.
- Regle 2 : Garder le texte le plus proche possible de l'original.
- Regle 3 : Ne pas changer le ton du texte original.
- Regle 4 : Garder la langue dans laquelle le texte t'a ete tranmis.
"""

#---
# Public
#---

def llmcorrect_ollama_correct(text: str, model: str) -> str:
    """ simple ollama request
    """
    try:
        return cast(
            str,
            cast(
                Any,
                ollama.chat(
                    model       = model,
                    messages    = [{
                        "role": "user",
                        "content": f"{__PROMPT_OLLAMA}\n{text}",
                    }],
                ),
            )['message']['content'],
        )
    except httpx.ConnectError as err:
        raise LlmcorrectException(
            'unable to connect with Ollama o(x_x)o'
        ) from err
