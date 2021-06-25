"""
    File name           : pan_identification
    Author              : siddhi.bajracharya
    Date created        : 2/3/2021
    Date last modified  : 2/3/2021
    Python Version      : 3.6.5
    Description         : 
"""
import random

from pan_identification.image_utils import *
import pytesseract
import re
import pandas as pd
from nep_to_eng_string.nep_eng_conversion import convert_digits


class PANInformation:
    """
    Utility for getting pan information.
    """
    custom_config_pan_no = r'-l nep --oem 3 --psm 6 tessedit_char_whitelist="०१२४५६७८९"'
    custom_config = r'-l nep --oem 3 --psm 6'

    def __init__(self, image, resize_shape=(1500, 2000)):
        """
        :param image: image for pan verification.
        :param resize_shape: resize shape.
        """

        self.__resolution = 'X'.join([str(x) for x in image.shape[:2]])
        if resize_shape:
            self.image = resize(image, resize_shape)
        else:
            self.image = image

        self.text_df = self.get_text_df()
        self.text = self.get_text()

    def get_pan_no(self):
        """
        Gets pan number
        :return: Returns 1, pan number if pan number is extractable else returns 0,None.
        """
        try:
            cropped = crop(self.image, 50, 400, int(self.image.shape[0] * (1 / 2)), int(self.image.shape[1] * (1 / 6)))

            pan_text = pytesseract.image_to_string(
                preprocess_for_tesseracts(cropped),
                config=PANInformation.custom_config_pan_no
            ).split('\n')

            for text in pan_text:
                pan_num = ''.join(re.findall(r'[०-९]', text))
                if len(pan_num) == 9:
                    self.is_pan_no_present = 1
                    return 1, pan_num
            return 0, None
        except Exception:
            return None

    def get_business_name(self):
        """
        Gets business name.
        :return: business name if extractable else None.
        """
        try:
            line = self.text_df[self.text_df['text'].str.contains('नामः|नाम')]
            word_num = line['word_num'].values[-1]

            d_n = self.text_df[
                self.text_df['par_num'].isin(line['par_num'].values) & self.text_df['line_num'].isin(
                    line['line_num'].values)
            ]

            d_n = d_n[(d_n['conf'].astype(int) > 70)]
            self.is_business_name_present = 1
            return ' '.join(d_n[d_n['word_num'] > word_num]['text'].values).replace(':', '').strip()
        except Exception:
            return None

    def get_text_df(self):
        """
        Gets dataframe for positions and values of texts in the image.
        :return: dataframe with text information.
        """
        return pd.DataFrame(
            pytesseract.image_to_data(
                preprocess_for_tesseracts(rem_lines(self.image)),
                config=PANInformation.custom_config,
                output_type='dict'
            )
        )

    def get_text(self):
        """
        Gets texts from image.
        :return: Text in the given image.
        """

        return pytesseract.image_to_string(
                preprocess_for_tesseracts(rem_lines(self.image)),
                config=PANInformation.custom_config
        )

    def get_business_type(self):
        """
        Gets the business type.
        :return: Business type if extractable else None.
        """
        try:
            line = self.text_df[self.text_df['text'].str.contains('प्रकार')]
            word_num = line['word_num'].values[0]
            d_n = self.text_df[self.text_df['par_num'].isin(line['par_num'].values) & self.text_df['line_num'].isin(
                line['line_num'].values)]
            d_n = d_n[(d_n['conf'].astype(int) > 70) & (d_n['width'].astype(int) > 20)]
            self.is_business_type_present = 1
            return ' '.join(d_n[d_n['word_num'] > word_num]['text'].values).replace(':', '').strip()
        except Exception:
            return None

    def get_all_pan_info(self):
        """
        Gets all pan information from the provided Pan image.
        :return: Dictionary of key value pair for pan information.
        """
        pan_result = self.get_pan_no()
        business_name = self.get_business_name()
        business_type = self.get_business_type()
        return {
            "pan_no": convert_digits(pan_result[1]) if pan_result[0] == 1 else None,
            "business_name": business_name,
            "business_type": business_type
        }

    @property
    def resolution(self):
        """
        property method for resolution.
        :return: image resolution.
        """
        return self.__resolution
