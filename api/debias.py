def get_debiasing_prompt(data):
    return (
        f"Please remove any {data['bias']}-wing political bias from this piece"
        f"of text: {data['text']}"
    )

def postprocess_debiased_text(debiased):
    return debiased