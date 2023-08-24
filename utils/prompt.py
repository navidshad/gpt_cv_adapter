def evaluate_promp_result(result):
    if not result:
        return False

    starters = ["```html", "```json", "```plaintext", "```markdown", "```md", "```"]
    enders = ["```"]

    for starter in starters:
        if result.startswith(starter):
            result = result[len(starter) :]

    for ender in enders:
        if result.endswith(ender):
            result = result[: -len(ender)]

    return result
