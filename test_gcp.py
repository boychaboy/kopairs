# from google.cloud import translate_v3beta1 as translate

# client = translate.TranslationServiceClient()
# response = client.translate_text(
    # parent=parent,
    # contents=["안녕하세요"],
    # mime_type='text/plain',  # mime types: text/plain, text/html
    # source_language_code='ko',
    # target_language_code='ja')

# for translation in response.translations:
    # print('Translated Text: {}'.format(translation))

from google.cloud import translate_v2 as translate

client = translate.Client()
result = client.translate('안녕하세요', target_language='ja')
print(result['translatedText'])
