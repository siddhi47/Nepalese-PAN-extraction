"""
    File name           : pan_verification
    Author              : siddhi.bajracharya
    Date created        : 2/11/2021
    Date last modified  : 2/11/2021
    Python Version      : 3.6.5
    Description         : 
"""


class PANVerification:
    """
    Class for pan verification
    """
    def __init__(self, info_dict, table, session):
        """

        :param info_dict: information dictionary containing key value pair of pan details.
        :param table: Table from where verification is to be made.
        :param session: database session.
        """
        self.info_dict = info_dict
        self.table = table
        self.table_name = table.__table__.name
        self.session = session
        if self.info_dict['pan_no'] is None:
            raise ValueError("PAN is None. PAN number cannot be None.")

    def verify_pan_no(self):
        """
        verify the pan number
        :return: pan number if verification is successful else None.
        """
        res = self.session.execute(
            self.session.query(self.table.pan_no).filter(self.table.pan_no == self.info_dict['pan_no'])
        )
        if res:
            return self.info_dict['pan_no']
        else:
            return None

    # TODO: verification of business type.
    def verify_business_type(self):
        pass

    # TODO: verification of business name.
    def verify_business_name(self):
        pass

    def verify_from_internal(self):
        """
        Internal verification from fonepay server.
        :return: 1 if successful else 0
        """
        pan = self.verify_pan_no()
        if pan is not None:
            return 1
        else:
            return 0

    def verify(self):
        """
        Generalized verification method.
        :return: 1 if verification successful else 0.
        """
        if self.table_name == 'ocr_ird_pan_details':
            return self.verify_from_IRD()
        elif self.table_name == 'ocr_pan_details':
            return self.verify_from_internal()
        else:
            raise ValueError("Invalid verification from {}".format(self.table_name))


    def verify_from_IRD(self):
        """
        verification from IRD database.
        :return: 1 if verification successful else 0.
        """
        pan = self.verify_pan_no()
        if pan is not None:
            return 1
        else:
            return 0
