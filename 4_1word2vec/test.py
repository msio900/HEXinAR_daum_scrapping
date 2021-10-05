import pickle

with open("피클 파일 경로", "rb") as r: #피클파일경로 입력
    read_data=pickle.load(r)


def similarity_word(data):
    search_word = '달고나'# data
    w2v_model_result = read_data.wv.most_similar(search_word, topn=30)

    sim_words = []
    for i in w2v_model_result:
        sim_word = i[0].replace(',','')
        # print(sim_words)
        sim_words.append([search_word, sim_word])

    return sim_words

if __name__ == "__main__":
    print(similarity_word("달고나"))


