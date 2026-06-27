"""4 subagent: challenge / solve (strong+weak) / verify_cot."""
import json
import re

from llm_client import call_llm
from prompts import CONTEXTS, CHALLENGER_PROMPT, STRONG_SOLVER_PROMPT, WEAK_SOLVER_PROMPT, VERIFIER_PROMPT
from verifier import extract_answer


def _parse_json(text):
    """Lấy JSON đầu tiên trong text (LLM hay bọc trong ```json ... ```)."""
    if not text:
        return {}
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}


def challenge(seed, idx=0):
    ctx = CONTEXTS[idx % len(CONTEXTS)]  # luân phiên bối cảnh -> đa dạng chủ đề
    msgs = [{"role": "user", "content": CHALLENGER_PROMPT.format(
        seed_q=seed.question, seed_a=seed.answer, context=ctx)}]
    return _parse_json(call_llm("challenger", msgs, idx))  # {question, final_answer, topic}


def solve(question, role, idx=0):
    prompt = WEAK_SOLVER_PROMPT if role == "weak" else STRONG_SOLVER_PROMPT
    msgs = [{"role": "user", "content": prompt.format(question=question)}]
    out = call_llm(role, msgs, idx)
    return out, extract_answer(out)


def verify_cot(question, cot, answer, idx=0):
    msgs = [{"role": "user", "content": VERIFIER_PROMPT.format(question=question, cot=cot, answer=answer)}]
    return _parse_json(call_llm("verifier", msgs, idx))  # {valid, reason}
