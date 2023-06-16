import json
import openai
import time

from utils.data import build_corpus

openai.api_key = "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"


def get_seed_data(test_word_lists, path2):
    f2 = open(path2, 'a', encoding="utf-8")
    for line in test_word_lists:
        f2.write(f"{line}" + "\n")
        f2.flush()
    f2.close()


def encode_prompt(seed):
    """Encode multiple prompt instructions into a single string."""
    prompt = open("./models/chatgpt/prompt_template.txt", "r", encoding="utf-8").readlines()[0]
    prompt += f"{seed}" + " 对应标签："
    return prompt


def generate_instruction_following_data(seeds_path):
    seed_dialog = [l for l in open(seeds_path, "r", encoding="utf-8").readlines()]
    for id, seed in enumerate(seed_dialog):
        if id <= 145:
            print(id)
            continue
        prompt = encode_prompt(seed[:-1])
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                  messages=[{"role": "user", "content": prompt}])
        new_dialog = completion.choices[0].message.content
        print(id, new_dialog)
        with open("./model_outs/chatgpt/test_prev_tags.json", 'a', encoding="utf-8") as f:
            dialog_dict = {}
            dialog_dict["id"] = f"{id}"
            dialog_dict["dialog"] = new_dialog
            f.write(json.dumps(dialog_dict, ensure_ascii=False) + '\n')
            f.flush()
        time.sleep(22)


def main():
    test_word_lists, test_tag_lists = build_corpus("test", make_vocab=False)
    # get_seed_data(test_word_lists, "./model_outs/chatgpt/prompt_seeds.json")  # 生成prompt seeds
    # generate_instruction_following_data("./model_outs/chatgpt/prompt_seeds.json")  # 调用chatgpt api 在测试集上进行NER任务
    d = open("./model_outs/chatgpt/test_prev_tags.json", "r", encoding="utf-8").readlines()
    test_prev_tag_lists = []
    for l in d:
        tag_list = eval(json.loads(d[0])["dialog"])
        test_prev_tag_lists.append(tag_list)


if __name__ == "__main__":
    main()
