from src.get_xml import GetXML
from src.transform_xml import TransformXML

gx = GetXML()
gx.download_xml()

tx = TransformXML()
tx.write_csv()
