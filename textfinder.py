import fitz
import os
import json

def rect_to_tuple(rect):
    return (rect.x0, rect.y0, rect.x1, rect.y1)

def find_word_in_pdf(pdf_path, word):
    doc = fitz.open(pdf_path)
    sentences = []
    locations = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        locations.extend([rect_to_tuple(rect) for rect in page.search_for(word)])
        text = page.get_text()
        lines = text.split('.')
        for line in lines:
            if word.lower() in line.lower():
                sentences.append(line.strip())
    doc.close()
    return sentences, locations

def process_files_in_folder(folder_path, words_list):
    files_list = os.listdir(folder_path)
    result = {"files": []}
    for file in files_list:
        file_data = {"file_name": file, "words": []}
        for word in words_list:
            pdf_path = os.path.join(folder_path, file)
            sentences, locations = find_word_in_pdf(pdf_path, word)
            file_data["words"].append({"word_name": word, "instances": sentences, "locations": locations})
        result["files"].append(file_data)

    return result

if __name__ == "__main__":
    folder_path = 'pdfs'
    words_list = ['since', 'investment', 'capital']
    result = process_files_in_folder(folder_path, words_list)

    with open("result.json", "w") as json_file:
        json.dump(result, json_file, indent=4, default=rect_to_tuple)
