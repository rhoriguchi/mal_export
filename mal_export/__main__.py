import logging
import sys

from mal_export.export_type import ExportType
from mal_export.mal_extractor import MALExtractor


def main():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logging.basicConfig(level=logging.INFO, handlers=[console_handler])

    try:
        extractor = MALExtractor()

        anime_xml_content, mange_xml_content = extractor.get_anime_and_manga_xml_content()

        extractor.save_xml(ExportType.ANIME, anime_xml_content)
        extractor.save_xml(ExportType.MANGA, mange_xml_content)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as ex:
        logging.exception(ex)
        sys.exit()


if __name__ == '__main__':
    main()
