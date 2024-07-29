import json

json_file_path = './Nicholas-Mark-Hairdressing-Dataset.json'
jsonl_file_path = 'Nicholas-Mark-Hairdressing-Dataset.jsonl'

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

system_message = {"role": "system", "content": "Provide answers based on the input given for 'Nicholas_Mark_Hair_Salon'."}

with open(jsonl_file_path, 'w') as jsonl_file:
    for entry in data:
        question = entry["question"]
        answer = entry["answer"]
        messages = [
            system_message,
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ]
        jsonl_entry = {"messages": messages}
        jsonl_file.write(json.dumps(jsonl_entry) + '\n')

