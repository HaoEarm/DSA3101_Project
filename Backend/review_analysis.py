from flask import Flask, jsonify, request
import os
from openai import OpenAI
import pandas as pd
import constants

app = Flask(__name__)

# Read in data
# GXS_Apple = pd.read_csv('https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/GXS_Bank_Apple.csv', index_col=0)
# GXS_Google = pd.read_csv('https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/GXS_Bank_Google.csv', index_col=0)
# # Combine for Training Data
# df_merged = pd.concat([GXS_Apple, GXS_Google], ignore_index=True, sort=False)
# full_text = "\n".join([f"Score: {row['Score']}, Review: {[row['Review']]}, Date: {row['Date']}, Bank: {row['Bank']}" for index, row in df_merged.iterrows()])

df = pd.read_csv("https://raw.githubusercontent.com/HaoEarm/DSA3101_Project/main/Data/predictions.csv")
full_text = "\n".join([f"Score: {row['Score']}, Review: {[row['Review']]}, Date: {row['Date']}, Bank: {row['Bank']}" for index, row in df.iterrows()])

# @app.route('/custom_query', methods=['POST'])
# def custom_query():
#     try:
        # text_length = len(full_text)
        #
        # # Split the full_text into two halves
        # half_length = text_length // 2  # Use floor division to ensure integer result
        # first_half = full_text[:half_length]
        # second_half = full_text[half_length:]
        #
        # user_query = request.json['query']
        #
        # os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
        # client = OpenAI()
        #
        # completion = client.chat.completions.create(
        #     model="gpt-4-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant analyzing bank reviews. Respond based on the following reviews:"},
        #         {"role": "user", "content": first_half},
        #         {"role": "user", "content": second_half},
        #         {"role": "user", "content": user_query}
        #     ],
        # )
    #     generated_text = str(completion.choices[0].message.content)
    #     return jsonify({"response": generated_text})
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     return jsonify({"error": str(e)}), 500


@app.route('/custom_query', methods=['POST'])
def custom_query():
    try:
        text_length = len(full_text)

        first_15000 = full_text[:15000]
        # Split the full_text into two halves
        # half_length = text_length // 2  # Use floor division to ensure integer result
        # first_half = full_text[:half_length]
        # second_half = full_text[half_length:]

        user_query = request.json['query']

        os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant analyzing bank reviews. Respond based on the following reviews:"},
                {"role": "user", "content": first_15000},
                {"role": "user", "content": user_query}
            ],
        )
        generated_text = str(completion.choices[0].message.content)
        return jsonify({"response": generated_text})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

# @app.route('/custom_query', methods=['POST'])
# def custom_query():
#     try:
#         user_query = request.json['query']
#
#         os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
#         client = OpenAI()
#
#         # Split the full text into two paragraphs
#         full_text_paragraphs = full_text.split("\n\n")
#
#         # Send each paragraph separately
#         completion_results = []
#         for paragraph in full_text_paragraphs:
#             completion = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant analyzing bank reviews. Respond based on the following reviews:"},
#                     {"role": "user", "content": paragraph},
#                     {"role": "user", "content": user_query}
#                 ],
#             )
#             completion_results.append(str(completion.choices[0].message.content))
#
#         return jsonify({"responses": completion_results})
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return jsonify({"error": str(e)}), 500


# @app.route('/custom_query', methods=['POST'])
# def custom_query():
#     try:
#         first_60000 = full_text[:60000]
#         user_query = request.json['query']
#
#         os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
#         client = OpenAI()
#
#         # Split the full text into two paragraphs
#         full_text_paragraphs = first_60000.split("\n\n")
#
#         # Send each paragraph separately
#         completion_results = []
#         for paragraph in full_text_paragraphs:
#             completion = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant analyzing bank reviews. Respond based on the following reviews:"},
#                     {"role": "user", "content": paragraph},
#                     {"role": "user", "content": user_query}
#                 ],
#             )
#             completion_results.append(str(completion.choices[0].message.content))
#
#         return jsonify({"responses": completion_results})
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)