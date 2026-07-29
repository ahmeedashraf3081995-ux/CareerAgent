import PyPDF2


def extract_text(uploaded_file):

    text = ""


    reader = PyPDF2.PdfReader(
        uploaded_file
    )


    for page in reader.pages:

        content = page.extract_text()

        if content:

            text += content + "\n"



    return text