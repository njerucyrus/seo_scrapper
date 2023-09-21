import re

import scrapy
from langchain.document_loaders import WebBaseLoader


class DataSpiderSpider(scrapy.Spider):
    name = 'data_spider'

    def __init__(self, **kwargs):
        self.start_urls = [kwargs.get('url')]

    def parse(self, response):
        meta_tags = response.xpath('//meta')
        meta_tags_list = []
        for meta in meta_tags:
            meta_data = {}
            for key, value in meta.attrib.items():
                meta_data[key] = value
                meta_tags_list.append(meta_data)

        image_tags = response.xpath('//img')

        # Iterate through the image tags and extract their src and alt attributes
        image_list = []
        for img in image_tags:
            img_data = {}
            img_data['src'] = img.xpath('@src').get()
            img_data['alt'] = img.xpath('@alt').get()
            image_list.append(img_data)

        text = self.load_website_data(links=self.start_urls)
        yield {
            'meta_tags': meta_tags_list,
            'images': image_list,
            'text': text
        }

    def load_website_data(self, links):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }
        loader = WebBaseLoader(web_path=links, header_template=headers)
        docs = loader.load()
        cleaned_docs = []
        for doc in docs:
            content = doc.page_content
            cleaned_text = re.sub(r'\n+', '\n', content)
            cleaned_text = re.sub(r'\s+', ' ', content)

            cleaned_text = cleaned_text.strip()
            item = {
                'data': cleaned_text,
                'source': doc.metadata.get('source')
            }
            cleaned_docs.append(item)
        return cleaned_docs
