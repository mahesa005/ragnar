import fitz, pdfplumber

def extract_text(page: pdfplumber.page.Page) -> list:
    """
    extract text line with page coordinates
    input: page object
    output: every word in the page in a list 
            of strings with its coordinates saved
    """
    word_extracts = []
    page_words = page.extract_words()
    for word in page_words:
        content = word["text"]
        y = word["top"] # save top coordinate for sorting use
        coordinates = {"x0": word["x0"], "y0": word["top"], "x1": word["x1"], "y1": word["bottom"]}
        word_extracts.append(
             {
                  "type": "text",
                  "content": content,
                  "y": y,
                  "coordinates": coordinates
             }
        )
    return word_extracts
        

def extract_tables(page: pdfplumber.page.Page) -> list:
    """
    extract all tables from page
    input: page object
    output: all tables in page in form of list of 
            list of list (coordinates included)
    """
    table_extracts = []
    page_tables_content = page.extract_tables()
    page_tables_pos = page.find_tables()
    for table_content, table_pos in zip(page_tables_content, page_tables_pos):
        bbox = table_pos.bbox
        y = bbox[1]
        coordinates = {"x0": bbox[0], "y0": bbox[1], "x1": bbox[2], "y1": bbox[3]}
        table_extracts.append({
            "type": "table",
            "content": table_content,
            "y": y,
            "coordinates": coordinates
        })
    return table_extracts

def extract_images(page: fitz.Page) -> list:
    """
    extract all images from page
    input: page object
    output: all images from page in form of...
    """
    doc = page.parent
    image_extracts = []
    page_images = page.get_images(full=True)
    for img in page_images:
            # Get image bytes
            base_img = doc.extract_image(img[0])
            img_bytes = base_img["image"]

            # Get image coordinates
            img_rects = page.get_image_rects(img[0]) # make sure to align the coordinates with pdfplumber's coordinate system

            # Get y coordinate
            y = img_rects[0].y0 if img_rects else 0
            image_extracts.append({
                "type": "image",
                "content": img_bytes,
                "y": y,
                "coordinates": img_rects
            })
    return image_extracts

def extract_page(plumber_page: pdfplumber.page.Page, fitz_page: fitz.Page, page_num: int) -> list:
    """
    run text-table-image extraction pipeline on page
    input: plumber_page, fitz_page
    output: all elements combined with page_num as metada on each element
    """
    text = extract_text(plumber_page)
    tables = extract_tables(plumber_page)
    images = extract_images(fitz_page)

    all_elements = text + tables + images

    for element in all_elements:
        element["page_num"] = page_num

    # sort all elements base on y    
    all_elements.sort(key=lambda x: x["y"])
    return all_elements