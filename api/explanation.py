from chatgpt_wrapper import ChatGPT

def get_explainability_prompt(data):
    return (
        "Please identify certain phrases in an article that may indicate "
        f"{data['bias']}-wing political bias from an article with this "
        f"link: {data['url']}"
    )

def postprocess_explaination(explanation):
    return explanation


def explaination(data):
    bot = ChatGPT()
    print(data)
    prompt = get_explainability_prompt(data)
    print(prompt)
    ok, response, _ = bot.ask(prompt)
    

    bot._shutdown()

    return postprocess_explaination(response)


data = {
    'bias': 'left',
    'url': 'https://www.cnn.com/2023/04/14/politics/nra-convention-republican-2024-presidential-race/index.html'
}

out = explaination(data)

print(out)