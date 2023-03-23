from docx_utils.flatten import opc_to_flat_opc
import xml.dom.minidom


class Quizlet:
    BODY_TAG = 'w:body'
    FILTER = 'w:highlight'

    TEMP_XML = 'temp.xml'

    def __init__(self, path):
        # temp_xml = 'temp.xml'
        # opc_to_flat_opc('path', 'temp_xml')
        pass

    def xml_paragraphs(self, xml_file=TEMP_XML):

        domtree = xml.dom.minidom.parse('test.xml')
        root = domtree.documentElement
        body = root.getElementsByTagName(Quizlet.BODY_TAG)[0]
        xml_paragraphs = body.getElementsByTagName('w:p')

        return xml_paragraphs

    def filter_paragraphs(self, xml_paragraphs, filter=FILTER):
        filtered_xml_paragraphs = [
            xml_paragraph for xml_paragraph in xml_paragraphs if xml_paragraph.getElementsByTagName(filter)]

        highlighted = []

        for filtered_xml in filtered_xml_paragraphs:
            highlighted.append({'color': filtered_xml.getElementsByTagName(filter)[0].getAttribute('w:val'),
                                'text': filtered_xml.getElementsByTagName('w:t')[0].childNodes[0].nodeValue})
        
        return highlighted

    def convert_word_def(self, colors_texts):
      words_defs = []
      counter = -1
      sentence = ""
      for color_text in colors_texts:
        if color_text['color'] == 'cyan':
          words_defs.append({'word': color_text['text'], 'defs': []})
          counter += 1

        elif color_text['color'] == 'yellow':
          words_defs[counter]['defs'].append(color_text['text'])
      
      for word_def in words_defs:
        sentence += '{},{};'.format(word_def['word'], '\n'.join(word_def['defs']))

      return sentence
