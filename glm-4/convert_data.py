import json
import argparse


def load_data(infile):
    with open(infile, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def convert_to_jsonl(original_data, trainfile, devfile):
    _len = int(len(original_data) * 0.7)
    i = 0
    with open(trainfile, 'w', encoding='utf-8') as train_file, \
            open(devfile, 'w', encoding='utf-8') as dev_file:
        for item in original_data:
            messages = {
                "messages": [
                    {
                        "role": "user",
                        "content": item["q"]
                    },
                    {
                        "role": "assistant",
                        "content": item["a"]
                    }
                ]
            }
            i += 1
            if i < _len:
                train_file.write(json.dumps(
                    messages, ensure_ascii=False) + '\n')
            else:
                dev_file.write(json.dumps(
                    messages,
                    ensure_ascii=False) + '\n')


def txt2json(infile, outfile):
    with open(infile, 'r', encoding='utf-8') as file:
        data = file.read()
    lines = data.split('\n')
    json_data = []
    for i in range(len(lines)):
        if (i - 2 >= 0) and ((i - 2) % 3 == 0):
            question = lines[i-2]
            answer = lines[i-1]
            json_data.append({"q": question, "a": answer})
    with open(outfile, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', type=str, required=True)
    parser.add_argument('--trainfile', type=str, required=True)
    parser.add_argument('--devfile', type=str, required=True)
    args = parser.parse_args()
    # change text to json
    jsonOutFile = args.infile.replace(".txt", ".json")
    txt2json(args.infile, jsonOutFile)
    # splite json file
    original_data = load_data(jsonOutFile)
    convert_to_jsonl(original_data,
                     args.trainfile, args.devfile)
