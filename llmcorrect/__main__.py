"""
llmcorrect  - quick corrector assistant
"""
from typing import NoReturn, Optional
from pathlib import Path
import sys

import click
import pyperclip    # type: ignore

from llmcorrect.exception import LlmcorrectException
from llmcorrect._ollama import llmcorrect_ollama_correct

#---
# Internal
#---

@click.command('llmcorrect')
@click.argument('text', required = False)
@click.option(
    '-m', '--model', 'model',
    required    = False,
    metavar     = 'MODEL_NAME',
    default     = 'gemma',
    help        = 'change the default LLM model (gemma)',
)
@click.option(
    '-f', '--file', 'input_file',
    required    = False,
    metavar     = 'PATH',
    help        = 'file to correct',
    type        = click.Path(
        exists          = True,
        file_okay       = True,
        dir_okay        = False,
        readable        = True,
        resolve_path    = True,
        path_type       = Path,
    ),
)
@click.option(
    '-o', '--output', 'output_file',
    required    = False,
    metavar     = 'PATH',
    help        = 'file to export',
    type        = click.Path(
        exists          = False,
        resolve_path    = True,
        path_type       = Path,
    ),
)
def llmcorrect_cli_entry(
    text: Optional[str],
    model: str,
    input_file: Optional[Path],
    output_file: Optional[Path],
) -> NoReturn:
    """ correct the provided input (manual, clipboard, ...)
    """
    try:
        if not text:
            if input_file:
                with open(input_file, 'r', encoding='utf8') as input_fd:
                    text = input_fd.read()
            else:
                text = pyperclip.paste()
        if not text:
            print(
                '\033[0;33m'
                'WARNING: empty provided text, manual input'
                '\033[0m',
                file = sys.stderr,
            )
            if not (text := input()):
                raise LlmcorrectException('no text provided, abort')
        output = llmcorrect_ollama_correct(text, model)
        if output_file:
            output_file.touch()
            with open(output_file, 'w', encoding='utf-8') as output_fd:
                output_fd.write(output)
        else:
            pyperclip.copy(output)
        sys.exit(0)
    except LlmcorrectException as err:
        print(f"\033[0;31m{err}\033[0m", file=sys.stderr)
        sys.exit(1)

#---
# Public
#---

# Allow function invokation with missing parameters. Click will provide
# and handle missing parameters
# pylint: disable=locally-disabled,E1120
llmcorrect_cli_entry()
