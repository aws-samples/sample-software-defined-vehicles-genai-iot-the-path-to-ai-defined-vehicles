from flask import Flask, request

from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
import os
import sys


if len(sys.argv) < 2:
    print("Not enough arguments provided. Please invoke with port and path to the llm model as param 1 and param 2 respectively.")
    sys.exit(1)

args = sys.argv[1:]
port = args[0]
model_path = args[1]

print("Launching application server.py")
print(f"Port is {port}")
print(f"Model path is {model_path}")


#set the template for the model.
template = """<|system|>
You are an AI assistant for the car user guide. Cars have specifications and feature usage information that are available in the car specific user guide. You have been provided with the car user guide information.  You will be asked car questions pertaining to car specifications or car feature usage. The question will be only for cars even if there is no explicit mention of the word car or vehicle in the question. Please provide answers only from the car user guide data. You will provide a concise answer in two to three sentences maximum.</s>
<|user|>
{question}</s>
<|assistant|><|eot_id|>
"""

prompt = PromptTemplate.from_template(template)
# Load the model using LlamaCpp. We will set streaming=True to send the response out from the llm as the response tokens get generated, rather than waiting for the entire response. This is to provide faster response to the chat client application.
llm=LlamaCpp(model_path=model_path, use_mmap=False, temperature=0, n_ctx=2048, model_kwargs={"repetition_penalty": 2}, verbose=False, streaming=True, stop=['</s>','<|eot_id|>'])
llm_chain = prompt|llm

app = Flask(__name__)
@app.route('/llm', methods=['POST'])
def generate_llm_response():
    app.logger.info("Request received")
    question = request.form['input']
    app.logger.info(f"Input: {question}")
    def generate():
        for chunk in llm_chain.stream({"question": question}):
            #yeild the chunk for the client to use.
            yield chunk

    return generate(), {"Content-Type": "text/plain"}

if __name__ == '__main__':
    app.run(host='localhost', port=port, debug=False)
