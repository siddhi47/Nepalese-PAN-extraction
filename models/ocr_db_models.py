"""
    File name           : ocr_db_models.py
    Author              : siddhi.bajracharya
    Date created        : 2/11/2021
    Date last modified  : 2/11/2021
    Python Version      : 3.6.5
    Description         : 
"""

from sqlalchemy.ext.automap import automap_base
from utils.variables import var

Base = automap_base()
Base.prepare(var.engine, reflect=True)

IRD_DETAILS = Base.classes.ocr_ird_pan_details
PAN_DETAILS = Base.classes.ocr_pan_details
PAN_RESULTS = Base.classes.ocr_pan_results
PAN_VERIFICATION = Base.classes.ocr_verification
