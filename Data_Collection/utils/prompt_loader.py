# utils/prompt_loader.py

import os


def load_base_prompt(path="prompts/base_prompts.txt") -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Base prompt file not found: {path}")

    with open(path, "r") as f:
        return f.read().strip()


def load_instruction_block(path="prompts/instruction_block.txt") -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Instruction block file not found: {path}")

    with open(path, "r") as f:
        return f.read().strip()