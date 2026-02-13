import json
import re
import ast

def _strip_code_fence_and_whitespace(s: str) -> str:
    """去除常见的包裹（```json ... ```）、BOM、前后空白和非打印控制字符。"""
    if not isinstance(s, str):
        # 尝试把 bytes 解码为 str
        try:
            s = s.decode('utf-8')
        except Exception:
            s = str(s)
    # remove BOM
    s = s.lstrip('\ufeff\ufeff')
    # remove markdown fences like ```json ... ``` or ``` ... ```
    s = re.sub(r'^\s*```(?:json)?\s*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s*```\s*$', '', s)
    # remove single backticks that sometimes wrap inline JSON
    s = s.strip()
    if s.startswith('`') and s.endswith('`'):
        s = s[1:-1].strip()
    # remove common "non-json" prefix/suffix lines (like "Output:" or "Result:")
    s = re.sub(r'^[A-Za-z ]{0,20}:\s*\n', '', s)
    # remove zero-width and other control chars
    s = ''.join(ch for ch in s if ord(ch) >= 9)
    return s

def robust_parse(raw_output: str, raise_on_fail: bool = False):
    """尝试多步解析 LLM 输出，返回 Python 对象或 None（并打印诊断）。"""
    if raw_output is None:
        if raise_on_fail:
            raise ValueError("raw_output is None")
        return None

    # quick diagnostic: show repr prefix to catch invisible chars
    preview = repr(raw_output)[:500]
    # Attempt 0: quick clean of fences and whitespace
    candidate = _strip_code_fence_and_whitespace(raw_output)
    try:
        return json.loads(candidate)
    except Exception as e0:
        # Attempt 1: remove trailing commas inside objects/arrays
        candidate2 = re.sub(r',\s*(\]|\})', r'\1', candidate)
        try:
            return json.loads(candidate2)
        except Exception as e1:
            # Attempt 2: if JSON uses single quotes or Python literals, try ast.literal_eval
            try:
                # convert JSON null/true/false -> Python None/True/False for ast
                py_like = candidate2.replace('null', 'None').replace('true', 'True').replace('false', 'False')
                return ast.literal_eval(py_like)
            except Exception as e2:
                # diagnostics: print short info to help you see what's wrong
                print("=== robust_parse DIAGNOSTIC ===")
                print("raw_output repr preview:\n", preview)
                print("candidate (after stripping fences) repr preview:\n", repr(candidate)[:500])
                print("error json.loads(candidate):", repr(e0))
                print("error json.loads(candidate2):", repr(e1))
                print("error ast.literal_eval:", repr(e2))
                print("=== END diagnostic ===")
                if raise_on_fail:
                    raise ValueError("Failed to parse LLM output as JSON/Python literal")
                return None
