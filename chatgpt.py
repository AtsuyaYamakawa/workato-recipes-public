import openai
import os
import constants
import datetime
import json

openai.api_key = constants.APIKEY
messages = []
message = ""
line = ""
model = "gpt-4"
print("model: " + model)
while True:
    line = input ("👤 You: ")
    if line == "bye":
        break
    while True:
      try:
        message += line + "\n"
        line = input()
      except EOFError:
        break
    messages.append ({"role": "user", "content": message})

    print("---\n🤖 ChatGPT(" + model + "): ")
    response = openai.ChatCompletion.create(
      model = model,
      messages = messages,
      stream=True  
    )
    collected_chunks = []
    collected_messages = []
    for chunk in response:
      content=chunk["choices"][0].get("delta",{}).get("content")
      if content is not None:
        print(content, end='')
        chunk_message = chunk['choices'][0]['delta']  # extract the message
        collected_messages.append(chunk_message)  # save the message
    print("\n---")
    full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
    messages.append({"role": "assistant", "content": full_reply_content})
    

save_conversation = input("---\n🤖 ChatGPT(" + model + "): 会話履歴を保存しますか？(y/n): ")
if save_conversation == "y":
    messages.append(
        {"role": "system", "content": "これまでの会話内容のタイトルを30文字以内でつけてください。"},
    )

    # Retrieve response from ChatGPT API using 'openai' library.
    title = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )["choices"][0]["message"]["content"].strip()

    file_name = title + "_" + datetime.datetime.now().strftime("%Y%m%dT%H%M") + ".txt"
    file_path = os.path.join("/Users/atsuya/code/chatgpt/logs/", file_name)

    with open(file_path, "w") as file:
        file.write(json.dumps(messages, ensure_ascii=False))
    print("---\n🤖 ChatGPT(" + model + "): 会話履歴を" + file_path + "に保存しました！\n---")