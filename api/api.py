import json 

from flask import (
    Flask,
    request,
    jsonify,
)

from flask_cors import CORS

from detection import (
    get_tokenizer, 
    get_model,
    detect_bias
)

app = Flask(__name__)
CORS(app)

models = {
    'detection': None
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

    return

@app.route('/detection', methods=['GET', 'POST'])
def detect_bias_endpoint(): 
    """ Submits survey data to SQL database. """
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