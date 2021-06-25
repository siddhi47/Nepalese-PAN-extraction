#! /venv/Scripts python

import sys
import math

import pandas as pd
from sqlalchemy.orm import Session

from models.ocr_db_models import *
from nep_to_eng_string.nep_eng_conversion import transliterate
from pan_identification.image_utils import *
from pan_identification.pan_identification import PANInformation
from pan_identification.pan_verification import PANVerification
from utils.logger import logger
from sqlalchemy.dialects import mysql


def get_raw_query(qry_object):
    """
    Get raw query from sqlalchemy query object
    :param qry_object: sqlalchemy query object
    :return: raw query
    """
    return qry_object.statement.compile(dialect=mysql.dialect())


def check_image_file(image_path):
    """
    Check if image file exists.
    :param image_path: image file path.
    :return: image file path if path is valid, else raise error.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File does not exist at {image_path}")
    return image_path


def get_file_list(path):
    """
    get list of files.
    :param path: directory path.
    :return: list of files in the given path.
    """
    path_list = []
    for path, _, files in os.walk(path):
        for name in files:
            path_list.append(os.path.join(path, name))
    return path_list


def write_to_db(pan_info_list, file_list, table):
    """
    write to database.
    :param pan_info_list: pan information list
    :param file_list: list of files.
    :param table: table name.
    :return: None
    """
    df = pd.DataFrame(
        columns=['file_path',
                 'pan_no',
                 'business_name',
                 'business_name_nepali',
                 'business_type',
                 'business_type_nepali',
                 'remarks',
                 'created_by'
                 ]
    )
    df['file_path'] = file_list
    df['pan_no'] = [x['pan_no'] for x in pan_info_list]
    df['business_type_nepali'] = [x['business_type'] for x in pan_info_list]
    df['business_name_nepali'] = [x['business_name'] for x in pan_info_list]
    df['business_name'] = df['business_name_nepali'].apply(transliterate)
    df['business_type'] = df['business_type_nepali'].apply(transliterate)
    df['image_resolution'] = [x['image_resolution'] for x in pan_info_list]

    try:
        var.engine.execute(f"TRUNCATE {table};")
        df.to_sql(table, var.engine, if_exists='append', index=False,)
    except Exception as e:
        raise Exception(f"Error while writing to database.\nError : {str(e)}")


def load_pan_info(path):
    """
    Loads pan information
    :param path: file path of image.
    :return:
    """
    # load image paths
    try:
        file_list = get_file_list(path)
        pan_info_list = []
        for file in file_list:
            logger.info(f"Reading File {file}")
            image = read_image(check_image_file(file))
            pan_info = PANInformation(image)

            pan_info_dict = pan_info.get_all_pan_info()
            pan_info_dict.update({'image_resolution': pan_info.resolution})

            pan_info_list.append(pan_info_dict)
        write_to_db(pan_info_list, file_list, PAN_RESULTS.__table__.name)
        logger.info("Write successful")
    except Exception as e:
        raise Exception(f"Error Loadinng PAN information. Error : {str(e)}")


def get_pan_info_dict(need_verification_row):
    """
    get pan information dictionary.
    :param need_verification_row: pandas row for verification of pan.
    :return: dictionary of pan information.
    """
    try:
        return {
            "pan_no":need_verification_row['ocr_pan_results_pan_no'],
            "business_type": need_verification_row['ocr_pan_results_business_type'],
            "business_name": need_verification_row['ocr_pan_results_business_name']
        }
    except Exception as e:
        raise Exception(f"Error getting dictionary from rows. Error : {str(e)}")


# TODO: write function for individual verification
def verify_individual_pan(need_verification_row):
    """
    verification of individual pan.
    :param need_verification_row:  pandas row for verification of pan.
    :return: dictionary for inernal and ird result.
    """
    try:
        pan_verification_dict = get_pan_info_dict(need_verification_row)

        session = Session(var.engine)

        pan_verify_ird = PANVerification(pan_verification_dict, IRD_DETAILS, session)
        pan_verify_internal = PANVerification(pan_verification_dict, PAN_DETAILS, session)

        return {
            "internal": pan_verify_internal.verify(),
            "ird": pan_verify_ird.verify()
        }
    except Exception as e:
        raise Exception(f"Error verifying individual PAN. Error : {str(e)}")


# TODO: Complete function for verifying pan info.
def verify_pan_info():
    """
    Verify pan information.
    :return:
    """
    try:
        try:
            session = Session(var.engine)
            q = session.query(
                PAN_RESULTS
            ).join(
                PAN_VERIFICATION,
                PAN_RESULTS.id == PAN_VERIFICATION.pan_result_id, isouter = True
            ).filter(
                PAN_VERIFICATION.is_verified == None
            )

            result = session.execute(q)
            need_verification_df = pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            raise Exception(f"Error getting data for verification. Error : {str(e)}")

        for _, row in need_verification_df.iterrows():
            if row['ocr_pan_results_pan_no'] is None:
                logger.warning(f"No Valid Pan Number found for file {row['ocr_pan_results_file_path']}")
                continue
            if not math.isnan(row['ocr_pan_results_pan_no']):
                verification = verify_individual_pan(row)
                internal, ird = verification['internal'], verification['ird']
                is_verified = 0
                if internal and ird:
                    is_verified=1
                res_dict = {
                    'pan_result_id': [row['ocr_pan_results_id']],
                    'is_verified': [is_verified],
                    'is_ird_verified': [ird],
                    'is_internal_verified': [internal]
                }

                pd.DataFrame(res_dict).to_sql(PAN_VERIFICATION.__table__.name,
                                              con = var.engine,
                                              index = False,
                                              if_exists='append'
                                        )
            else:
                logger.warning(f"No Valid Pan Number found for file {row['ocr_pan_results_file_path']}")
    except Exception as e:
        raise Exception(f"Error in Verification. Error : {str(e)}")


if __name__ == '__main__':
    """
    Main function.
    """
    if sys.argv[1] == 'load':
        logger.info("Loading the image results into the database.")
        try:
            image_path = sys.argv[2]
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"{image_path} does not exists.")
            load_pan_info(image_path)
            logger.info("Loading images ended.")
        except IndexError:
            raise IndexError("No path has been provided")
    elif sys.argv[1] == 'verify':
        logger.info("Verification Process Started")
        var.engine.execute(f'TRUNCATE {PAN_VERIFICATION.__table__.name}')
        try:
            verify_pan_info()
            logger.info("Verification Process ended.")
        except Exception as e:
            raise Exception(f"Error in PAN verification. Error : {str(e)}")
