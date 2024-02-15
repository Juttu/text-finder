import fitz

def highlight_areas(pdf_path, areas):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        areas_for_page = [area for area in areas if area["page_number"] == page_num+1]
        page = doc.load_page(page_num)
        for area in areas_for_page:
            rect = fitz.Rect(area["x0"], area["y0"], area["x1"], area["y1"])
            highlight = page.add_rect_annot(rect)
            highlight.update()
            highlight.set_colors()
    pdf_path.replace(".pdf", "_highlighted.pdf")
    doc.save(pdf_path.replace(".pdf", "_highlighted.pdf").replace("pdfs/","highlighted_pdfs/"))
    doc.close()

def highlight_all_pdfs(result_json):
    for file in result_json["files"]:
        allLocationsList=[]
        file_path = "pdfs/"+file["file_name"]
        for word in file["words"]:
            allLocationsList.extend(word["locations"])
        highlight_areas(file_path,allLocationsList)
            