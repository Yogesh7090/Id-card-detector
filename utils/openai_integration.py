import openai

api_key = 'YOUR_API_KEY'

openai.api_key = api_key

def process_text_with_openai(text, query):
    # payload = {
    #     "model": "gpt-4",
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": query
    #         },
    #         {
    #             "role": "user",
                
    #             "content": text
    #         }
    #     ],
    #     "max_tokens": 1000
    # }

    # response = openai.ChatCompletion.create(**payload)

    # if response:
    #     return response['choices'][0]['message']['content']
    # else:
    #     print(f"Error: {response}")
    #     return None

    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": query},
                            {"role": "user", "content": text}
                        ],
                        temperature=0,
                        max_tokens=1000, 
                        seed= 123       
                    )
                    # Extract and parse the ranked list from the GPT-3 response
    response_to_show_in_UI = response.choices[0].message.content

    return response_to_show_in_UI