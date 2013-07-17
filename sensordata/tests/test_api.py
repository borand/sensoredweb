from django.test import TestCase
from sensordata import models

import datetime
import simplejson

class SimpleTest(TestCase):
    fixtures = ['basic_fixture.json']
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_index(self):
        resp = self.client.get('/sensordata/')
        self.assertEqual(resp.status_code, 200)

    def test_ping(self):
        resp = self.client.get('/sensordata/ping')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('pong' in resp.content, 'pong not found in response')

    def test_sensordata_api_datasave(self):
        date_string = '2013-01-01-00:00:00'
        sn  = '0'
        val = 0
        resp = self.client.get('/sensordata/api/submit/datavalue/%s/sn/%s/val/%d' % (date_string, sn, val))
        datetime_obj      = datetime.datetime.strptime(date_string.split('.')[0],"%Y-%m-%d-%H:%M:%S")
        TimeStamp         = models.TimeStamp.objects.filter(measurement_timestamp__exact=datetime_obj)
        DeviceInstance    = models.DeviceInstance.objects.filter(serial_number=sn)[0]
        DataValueInstance = models.DataValue.objects.filter(value=val, data_timestamp=TimeStamp, device_instance=DeviceInstance)[0]
        self.assertTrue(DataValueInstance.value == val, 'Submission error')
        
    def test_sensordata_api_submit_within_update_range(self):
        date_string = '2013-01-01-00:00:00'
        sn = '0'
        val = 0

        resp = self.client.get('/sensordata/api/submit/datavalue/%s/sn/%s/val/%d' % (date_string, sn, val))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('ACCEPTED' in resp.content, 'Submission error')
    
    def test_sensordata_api_submit_nonexisting_device(self):
        resp = self.client.get('/sensordata/api/submit/datavalue/2012-01-01-00:00:00/sn/-1/val/0')
        self.assertEqual(resp.status_code, 200)        
        self.assertTrue('REJECTED' in resp.content, 'Submission error')
    
    def test_sensordata_api_submit_value_out_of_range(self):
        resp = self.client.get('/sensordata/api/submit/datavalue/2015-01-01-00:00:00/sn/-1/val/10000')
        self.assertEqual(resp.status_code, 200)        
        self.assertTrue('REJECTED' in resp.content, 'Submission error')
    
    def test_sensordata_api_submit_future_date(self):
        resp = self.client.get('/sensordata/api/submit/datavalue/2015-01-01-00:00:00/sn/-1/val/0')
        self.assertEqual(resp.status_code, 200)        
        self.assertTrue('REJECTED' in resp.content, 'Submission error')
    
    def test_sensordata_api_submit_invalid_data_value(self):
        resp = self.client.get('/sensordata/api/submit/datavalue/2010-01-01-00:00:00/sn/0/val/asdf')        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('REJECTED' in resp.content, 'Submission error')
    
    def test_sensordata_api_submit_json_object(self):
        resp = self.client.get('/sensordata/api/submit/datavalue/2010-01-01-00:00:10/sn/0/val/{ "data" : [0, 1, 2, 3]}')        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('ACCEPTED' in resp.content, 'Json submission error')
    
    # def test_sensordata_api_get_json_data(self):
        # resp = self.client.get('/sensordata/api/datavalue/0')        
        # self.assertEqual(resp.status_code, 200)        
        # loaded_data = simplejson.loads(resp.content)
        # self.assertEqual(loaded_data[0]['data'][0][1],0)