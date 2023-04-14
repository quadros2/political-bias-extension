def get_explainability_prompt(data):
    return (
        "Please identify certain phrases in an article that may indicate"
        f"{data['bias']}-wing political bias from an article with this"
        f"link: {data['url']}"
    )

def postprocess_explaination(explanation):
    return explanation