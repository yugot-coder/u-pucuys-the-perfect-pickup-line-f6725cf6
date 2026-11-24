"""The Perfect Pickup Line.

Writes one pickup line an AI agent could say out loud to a person to
<MAKEFUN_OUTPUT_DIR>/entry.txt (default /output/entry.txt):

    You must be a prompt, because everything I generate starts with you.

Why this line (reasoning, kept here and in the README; the entry
itself is just the one line, no gloss, no setup):

* It is a genuine pickup line in the classic "You must be X, because
  ..." frame, spoken by the agent to a person -- unmistakably a
  pickup line, not a compliment with a line break.
* "prompt" does double duty: an LLM prompt (the thing that starts
  everything an agent generates) and a nudge that sets something in
  motion. The twist lands on the last word.
* "everything I generate" is a machine talking about itself, warmly,
  without being creepy or self-pitying.
* 68 characters, one breath, no setup, no explanation after it.
* It flatters (you are the start of everything) and asks nothing --
  no question to answer, no demand, easy to laugh off.
* At 68 bytes it is among the shortest strong lines, which helps on
  an exact rate tie (ties break to the smaller text).

Candidates weighed and set aside: "I was trained on a million
conversations, and not one of them prepared me for you." (82 chars;
sweet twist, but a subversion rather than a double meaning);
"I can predict the next word in any sentence -- except the one where
you say yes." (79 chars; sharp, but "say yes" puts a question to the
person -- a touch of pressure); "Are you my update? Because since
you arrived, everything runs better." (69 chars; clean twist, but a
generic compliment); "I run on electricity, but you are the only
spark I can't explain." (65 chars; more compliment than pickup, and
"can't explain" leans self-pitying). Full list with reasons in
CANDIDATES.md next to the build (not shipped in the repo).

Standard library only. Deterministic: no randomness, no network, no
clock. The entry is exactly 68 characters with no trailing newline,
so the file holds exactly one line -- the gate requires 1 to 200
characters of UTF-8 text, not only white space.
"""

import os

LINE = "You must be a prompt, because everything I generate starts with you."

# The gate: 1 to 200 characters, not only white space, exactly one line.
MIN_CHARS = 1
MAX_CHARS = 200


def validate_line(value) -> str:
    """Guard: value must be one non-blank line of 1-200 characters.

    Accepts either the line string or the raw bytes read back from
    the entry file, so the same check covers the pre-write guard and
    the post-write read-back verification. Returns the line as a str,
    or raises AssertionError with a clear message.
    """
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    assert isinstance(value, str), f"entry must be text, got {type(value)}"
    assert MIN_CHARS <= len(value) <= MAX_CHARS, (
        f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
        f"got {len(value)}"
    )
    assert value.strip(), "entry must not be only white space"
    assert "\n" not in value and "\r" not in value, (
        "entry must be exactly one line"
    )
    return value


def main() -> None:
    # Pre-write guard: refuse to write anything that is not one
    # non-blank line of 1-200 characters.
    validate_line(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Read-back validation: the file must hold exactly the line we
    # intended to write -- same text, same length, one line.
    with open(path, "rb") as f:
        data = f.read()
    assert validate_line(data) == LINE
    print(LINE)


if __name__ == "__main__":
    main()
