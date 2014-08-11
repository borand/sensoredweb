"""
This module contains 2 key function used in data submission:
"""
import datetime
import requests

from django.utils.log import getLogger

logger = getLogger("app")

from math import sin, pi
from sensordata import models
import simplejson


def get_existing_or_new(date_string, save=False):
    """
    Attempts to find the existing TimeStamp object in the databasse
    (exact match down to a second) if none found creates 
    """
    logger.debug("get_existing_or_new(date_string=%s, save=%d)" % (date_string, save))

    try:
        if 'now' in date_string:
            datetime_obj = datetime.datetime.now()
        else:
            datetime_obj = datetime.datetime.strptime(date_string.split('.')[0], "%Y-%m-%d-%H:%M:%S")

        logger.debug("\tsubmited time: %s" % str(datetime_obj))

        time_stamp = models.TimeStamp.objects.filter(measurement_timestamp__exact=datetime_obj)

        if len(time_stamp) == 0:
            logger.debug("\tno previous record with this timestamp found")
            time_stamp = models.TimeStamp()
            time_stamp.measurement_timestamp = datetime_obj
            if save:
                time_stamp.save()
        else:
            logger.debug("\tfound existing record with this timestamp")
            time_stamp = time_stamp[0]

    except ValueError:
        # TODO - This exception must be handeled better
        logger.error("\tException occured, creating default time stamp, this might not be what you want...")
        time_stamp = models.TimeStamp()
        time_stamp.now()
        if save:
            time_stamp.save()

    return time_stamp


def data_value_submission(datestamp, serial_number, data_value, remote_addr):
    """
    Handles submission of data from remote sensors into the data base.
    """

    msg = "  data_value_submission(%s, %s, %s, %s)" % (datestamp, serial_number, data_value, remote_addr)
    logger.debug(msg)

    DeviceInstanceList = models.DeviceInstance.objects.filter(serial_number=serial_number)

    if len(DeviceInstanceList) == 1:
        DeviceInstance = DeviceInstanceList[0]

        if DeviceInstance.accept_from_gateway_only:
            msg = 'remote_address=%s matches DeviceInstance.gateway.address=%s' % (
                remote_addr, DeviceInstance.gateway.address)
            logger.debug(msg)
            if remote_addr not in DeviceInstance.gateway.address:
                msg = '[REJECTED]: Can only submit data from parent gateway'
                logger.debug(msg)
                return msg

        if DeviceInstance.active:
            TimeStamp = get_existing_or_new(datestamp)

            if TimeStamp.measurement_timestamp > datetime.datetime.now():
                msg = '[REJECTED]: Cannot submit values with future dates'
            else:
                max_value = float(DeviceInstance.device.max_range)
                min_value = float(DeviceInstance.device.min_range)
                update_rate = float(DeviceInstance.device.update_rate)

                try:
                    data_value_float = float(data_value)

                    if data_value_float <= max_value and data_value_float >= min_value:

                        ExistingDataValue = models.DataValue.objects.filter(device_instance=DeviceInstance).order_by(
                            '-data_timestamp')
                        logger.debug("Found %d existing ExistingDataValue objects" % (ExistingDataValue.count()))

                        if ExistingDataValue.count() > 0:
                            delta_time = TimeStamp.measurement_timestamp - ExistingDataValue[
                                0].data_timestamp.measurement_timestamp
                            delta_time_sec = float(delta_time.seconds)
                            last_data_value_float = ExistingDataValue[0].value
                        else:
                            delta_time_sec = update_rate
                            last_data_value_float = 10e10

                        logger.debug("%d sec since last submisison" % (delta_time_sec))

                        if delta_time_sec < update_rate:
                            msg = "[REJECTED]: Maximum update rate = %d sec exceeded." % (update_rate)
                        else:
                            if len(ExistingDataValue.filter(value=data_value_float, data_timestamp=TimeStamp)) > 0:
                                msg = "[REJECTED]: Identical record already found in the data base, new submission rejected"
                            else:
                                if abs(data_value_float - last_data_value_float) >= DeviceInstance.update_threshold or delta_time_sec > 3600:
                                    TimeStamp.save()
                                    DataValueInstance = models.DataValue(value=data_value_float,
                                                                         data_timestamp=TimeStamp,
                                                                         device_instance=DeviceInstance)
                                    DataValueInstance.save()
                                    msg = "[ACCEPTED]"
                                    logger.debug(msg)
                                    return msg
                                else:
                                    msg = '[REJECTED]: value has not changed by minimum update threshold within the past hour'
                                    logger.debug(msg)
                                    return msg

                    else:
                        msg = "  [REJECTED]: Value submitted is out of range [%f %f]" % (min_value, max_value)

                except ValueError:
                    logger.debug("Cannot convert to float attempting to decode JSON")

                    try:
                        submitted_obj = simplejson.loads(data_value)
                        logger.debug("Decoded submitted_obj")
                        ExistingDataValue = models.DataObject.objects.filter(device_instance=DeviceInstance).order_by(
                            '-data_timestamp')
                        logger.debug("Found %d existing ExistingDataValue objects" % (ExistingDataValue.count()))
                        if ExistingDataValue.count() > 0:
                            delta_time = TimeStamp.measurement_timestamp - ExistingDataValue[
                                0].data_timestamp.measurement_timestamp
                            delta_time_sec = float(delta_time.seconds)
                        else:
                            delta_time_sec = update_rate

                        logger.debug("%d sec since last submisison" % (delta_time_sec))
                        if delta_time_sec < update_rate:
                            msg = "[REJECTED]: Maximum update rate = %d sec exceeded." % (update_rate)
                        else:
                            TimeStamp.save()
                            DataValueInstance = models.DataObject(value=data_value, \
                                                                  data_timestamp=TimeStamp, \
                                                                  device_instance=DeviceInstance, \
                                                                  format="JSON")
                            DataValueInstance.save()
                            msg = "[ACCEPTED]"
                            logger.debug(msg)
                            return msg
                    except:
                        msg = '  [REJECTED]: Error during JSON decoding'

        else:
            msg = "  [REJECTED]: Device is not active, data will not be saved"
    else:
        msg = "  [REJECTED]: Device serial_number %s, NOT FOUND IN DB" % serial_number
    logger.debug(msg)
    return msg


if __name__ == '__main__':
    pass
    
