# visionインポート
from google.cloud import vision

with open('./領収書.jpg', 'rb') as image_file:
    content = image_file.read()

#vision APIが扱える画像データにする
image = vision.Image(content=content)

#ImageAnnotatorClientのインスタンスを生成
annotator_client = vision.ImageAnnotatorClient()

response_data = annotator_client.document_text_detection(image=image, image_context={'language_hints': ['ja']})

print('-----RESULT------')
output_text=''
for page in response_data.full_text_annotation.pages:
    for block in page.blocks:
        for paragraph in block.paragraphs:
            for word in paragraph.words:
                output_text += ''.join([symbol.text for symbol in word.symbols])
                output_text += '\n'
print(output_text)

print('-----RESULT------')

