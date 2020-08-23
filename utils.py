import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class NoRelevantHistoryPropertiesExc(Exception):
    pass


def calculate_percentile_for_property(yad2_row: object, relevant_records_for_average: list) -> float:
    logging_num_of_relevant_prop_for_avg(relevant_records_for_average)
    if not relevant_records_for_average:
        raise NoRelevantHistoryPropertiesExc('no relevant history prop to compare')
    yad2_prop_price_per_meter = float(yad2_row['price']) / float(yad2_row['size'])
    logger.info(f'yad2_prop_price_per_meter={yad2_prop_price_per_meter}')

    value_per_meter_list = []
    for rec in relevant_records_for_average:
        weighted_value = float(rec.declared_value) / float(rec.ground_ratio)

        if float(rec.size) != 0:
            val_per_meter = weighted_value / float(rec.size)
            value_per_meter_list.append(val_per_meter)
        else:
            logger.warning('got property in history records with size of 0')

    avg_value_per_meter = sum(value_per_meter_list) / len(value_per_meter_list)
    logger.info(f'avg_value_per_meter={avg_value_per_meter}')

    yad2_property_percentile = yad2_prop_price_per_meter / avg_value_per_meter
    logger.info(f'yad2_property_percentile={yad2_property_percentile}')

    if yad2_property_percentile <= 0.95:
        logger.info(f'Found Potential property! at {yad2_row["address"]}')

    return yad2_property_percentile * 100


def logging_num_of_relevant_prop_for_avg(relevant_records_for_average):
    num_of_relevant_records = len(relevant_records_for_average)
    if num_of_relevant_records == 0:
        logger.warning(f'0 records to calculate avg')
    if num_of_relevant_records < 4:
        logger.warning(f'basing on average of "{num_of_relevant_records}" records')
    else:
        logger.info(f'basing on average of "{num_of_relevant_records}" records')
