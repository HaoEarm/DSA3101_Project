from flask import Flask, jsonify, request
import os
from openai import OpenAI
import pandas as pd
import constants

app = Flask(__name__)

# Read in data
GXS_Apple = pd.read_csv('https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/GXS_Bank_Apple.csv', index_col=0)
GXS_Google = pd.read_csv('https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/GXS_Bank_Google.csv', index_col=0)
# Combine for Training Data
df_merged = pd.concat([GXS_Apple, GXS_Google], ignore_index=True, sort=False)
full_text = "\n".join([f"Score: {row['Score']}, Review: {[row['Review']]}, Date: {row['Date']}, Bank: {row['Bank']}" for index, row in df_merged.iterrows()])

@app.route('/analyze_reviews', methods=['GET'])
def analyze_reviews():
    try:
        os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
        client = OpenAI()

        completion = client.chat.completions.create(
            model = "gpt-4-turbo",
            messages= [{"role":"system", "content": """You are a helpful assisstant and you will be given the reviews for a bank application from users. 
                Your job is to summarize 5 categories of the negative comments and provide 5 recommendations in bullet point format 
                without using new lines or line breaks."
        """},
                {"role":"user","content":full_text[:]}],
    )
        generated_text = str(completion.choices[0].message.content)
        #cleaned_text = generated_text.replace("\\n", "\n")  # Replace escaped newlines with spaces
        #return jsonify({"analysis": cleaned_text})

        #formatted_text = generated_text.encode().decode('unicode_escape')
        #return jsonify({"analysis": formatted_text})
        return jsonify({"analysis": generated_text})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
@app.route('/index_statistics', methods=['GET'])
def index_statistics():
    try:
        os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
        client = OpenAI()

        completion = client.chat.completions.create(
            model = "gpt-4-turbo",
            messages= [{"role":"system", "content": """You are a helpful assisstant and you will be given the reviews for a bank application from users. 
                Your job is give statistics of the data like the average score, and the numbers etc. You can give any related data about numbers but do not include the calculation process, give the result directly"
        """},
                {"role":"user","content":full_text[:]}],
    )
        generated_text = str(completion.choices[0].message.content)
        return jsonify({"analysis": generated_text})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)

