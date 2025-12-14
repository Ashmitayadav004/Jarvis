from openai import OpenAI

# client = OpenAI()
client = OpenAI(
    api_key="",
)
completion = client.chat.completions.create(
    model ="gpt-3.5-turbo",
    messages=[
        {"role":"system" , "content":"You are virtual assisstant "},
        {"role":"user","content":"what is coding"}
    ]

)
print(completion.choices[0].message.content)