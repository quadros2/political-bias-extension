import os
import json 

from flask_cors import CORS
from flask import (
    Flask,
    request,
    jsonify,
)

from detection import (
    get_tokenizer, 
    get_model,
    detect_bias
)

from explanation import get_explainability_prompt, postprocess_explaination
from debias import get_debiasing_prompt, postprocess_debiased_text

from chatgpt_wrapper import OpenAIAPI

app = Flask(__name__)
CORS(app)

models = {
    'detection': None,
    'chatgpt': None
}

def setup_model(model_name, **kwargs):
    if model_name == "detection":
        tokenizer_name = kwargs.get("tokenizer_name", "bert-base-cased")
        model_name = kwargs.get("model_name", "bucketresearch/politicalBiasBERT")
        device = kwargs.get("device", "cpu")

        models[model_name] = (
            get_model(model_name, device),
            get_tokenizer(tokenizer_name)
        )
    
    elif model_name == "chatgpt":
        api_key_file = kwargs.get("api_key_file", "secret.key")
        with open(api_key_file, "r") as f:
            api_key = f.readline().strip()
            os.environ["OPENAI_API_KEY"] = api_key

        bot = OpenAIAPI()
        models[model_name] = bot

    return


@app.route('/detection', methods=['GET', 'POST'])
def detect_bias_endpoint(): 
    """ Gets bias from classification model """
    if request.method == "POST":
        data = request.data
        if data:
            data = json.loads(data.decode("utf-8"))

            if not models['detection']:
                setup_model("detection")

            bias = detect_bias(data['text'], *models['detection'])

            response = jsonify({
                'text': data['text'],
                'bias': bias
            })

            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        return "Invalid input"
    

@app.route('/explaination', methods=['GET', 'POST'])
def explain_bias_endpoint(): 
    """ Gets explanation of bias from ChatGPT """
    if request.method == "POST":
        data = request.data
        if data:
            data = json.loads(data.decode("utf-8"))

            # TODO(): get prompt for explanation
            explainability_prompt = get_explainability_prompt()
            success, explanation, message = models['chatgpt'].ask(explainability_prompt)
            if not success:
                return message
            
            # TODO(): postprocess explanation
            explanation = postprocess_explaination(explanation)
            
            response = jsonify({
                'text': data['text'],
                'explanation': explanation
            })

            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        return "Invalid input"
    

@app.route('/debias', methods=['GET', 'POST'])
def debias_endpoint(): 
    """ Debiases text through ChatGPT """
    if request.method == "POST":
        data = request.data
        if data:
            data = json.loads(data.decode("utf-8"))

            # TODO(): get prompt for debiasing
            debiasing_prompt = get_debiasing_prompt()
            success, debiased, message = models['chatgpt'].ask(debiasing_prompt)
            if not success:
                return message
            
            # TODO(): postprocess debiased text
            debiased = postprocess_debiased_text(debiased)
            
            response = jsonify({
                'text': data['text'],
                'debiased': debiased
            })

            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        return "Invalid input"