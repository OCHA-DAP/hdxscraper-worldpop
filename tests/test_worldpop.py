#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Unit tests for worldpop.

'''
from os.path import join

import pytest
from hdx.hdx_configuration import Configuration
from hdx.hdx_locations import Locations

from worldpop import generate_dataset_and_showcase, get_countriesdata


class TestWorldPop:
    countrydata = {'Source': 'WorldPop, University of Southampton, UK',
                   'URL_image': 'http://www.worldpop.org.uk/data/WorldPop_data/AllContinents/ZWE-POP_500.JPG',
                   'fileFormat': 'zipped geotiff',
                   'Dataset Title': 'WorldPop Zimbabwe Population dataset',
                   'authorEmail': 'worldpop@geodata.soton.ac.uk',
                   'updateFrequency': 'Every year', 'id_no': '243', 'authorName': 'WorldPop',
                   'URL_datasetDetailsPage': 'http://www.worldpop.org.uk/data/WorldPop_data/AllContinents/ZWE-POP.txt',
                   'Description': 'These datasets provide estimates of population counts ... information.',
                   'Visibility': 'Public',
                   'tags': ['Population Statistics', 'WorldPop', 'University of Southampton'],
                   'lastModifiedDate': '2016-10-17T12:54:54+01:00',
                   'datasetDatePrecision': 'Year',
                   'URL_summaryPage': 'http://www.worldpop.org.uk/data/summary?contselect=Africa&countselect=Zimbabwe&typeselect=Population',
                   'URL_direct': 'http://www.worldpop.org.uk/data/hdx/?dataset=ZWE-POP',
                   'Dataset contains sub-national data': 'true',
                   'Organisation': 'WorldPop, University of Southampton, UK; www.worldpop.org',
                   'datasetDate': '2015-01-01T00:00:00+00:00',
                   'productionDate': '2013-01-01T00:00:00+00:00',
                   'License': 'Other',
                   'Define License': 'http://www.worldpop.org.uk/data/licence.txt',
                   'iso3': 'ZWE',
                   'maintainerName': 'WorldPop',
                   'Location': 'Zimbabwe',
                   'maintainerEmail': 'worldpop@geodata.soton.ac.uk'}

    @pytest.fixture(scope='function')
    def configuration(self):
        Configuration._create(hdx_read_only=True,
                              project_config_yaml=join('tests', 'config', 'project_configuration.yml'))
        Locations.set_validlocations([{'name': 'zwe', 'title': 'Zimbabwe'}])

    @pytest.fixture(scope='function')
    def downloader(self):
        class Response:
            @staticmethod
            def json():
                pass

        class Download:
            @staticmethod
            def download(url):
                response = Response()
                if url == 'http://lala/getJSON/':
                    def fn():
                        return {'worldPopData': [TestWorldPop.countrydata]}
                    response.json = fn
                elif url == 'http://www.worldpop.org.uk/data/licence.txt':
                    response.text = 'The WorldPop project aims to provide an open access archive of spatial ' \
                                   'demographic datasets ... at creativecommons.org.'
                return response
        return Download()

    def test_get_countriesdata(self, downloader):
        countriesdata = get_countriesdata('http://lala/getJSON/', downloader)
        assert countriesdata == [TestWorldPop.countrydata]

    def test_generate_dataset_and_showcase(self, configuration, downloader):
        dataset, showcase = generate_dataset_and_showcase(downloader, TestWorldPop.countrydata)
        assert dataset == {'dataset_source': 'WorldPop, University of Southampton, UK',
                           'notes': 'These datasets provide estimates of population counts ... information.',
                           'data_update_frequency': '365',
                           'name': 'worldpop-zimbabwe-population',
                           'license_other': 'The WorldPop project aims to provide an open access archive of spatial demographic datasets ... at creativecommons.org.',
                           'license_id': 'hdx-other',
                           'dataset_date': '01/01/2015',
                           'url': 'http://www.worldpop.org.uk/data/summary?contselect=Africa&countselect=Zimbabwe&typeselect=Population',
                           'tags': [{'name': 'Population Statistics'}, {'name': 'WorldPop'}, {'name': 'University of Southampton'}],
                           'subnational': False,
                           'groups': [{'name': 'zwe'}],
                           'maintainer': '37023db4-a571-4f28-8d1f-15f0353586af',
                           'owner_org': '3f077dff-1d05-484d-a7c2-4cb620f22689',
                           'methodology_other': 'Go to [WorldPop Dataset Summary Page](http://www.worldpop.org.uk/data/summary?contselect=Africa&countselect=Zimbabwe&typeselect=Population) for more information',
                           'private': False,
                           'methodology': 'Other',
                           'title': 'Zimbabwe - Population'}

        resources = dataset.get_resources()
        assert resources == [{'description': 'Go to [WorldPop Dataset Summary Page](http://www.worldpop.org.uk/data/summary?contselect=Africa&countselect=Zimbabwe&typeselect=Population) for more information',
                              'format': 'zipped geotiff',
                              'url': 'http://www.worldpop.org.uk/data/hdx/?dataset=ZWE-POP',
                              'name': 'WorldPop Zimbabwe Population'}]

        assert showcase == {'image_url': 'http://www.worldpop.org.uk/data/WorldPop_data/AllContinents/ZWE-POP_500.JPG',
                            'name': 'worldpop-zimbabwe-population-showcase',
                            'title': 'WorldPop Zimbabwe Summary Page',
                            'notes': 'Click the image on the right to go to the WorldPop summary page for the Zimbabwe dataset',
                            'url': 'http://www.worldpop.org.uk/data/summary?contselect=Africa&countselect=Zimbabwe&typeselect=Population',
                            'tags': [{'name': 'Population Statistics'}, {'name': 'WorldPop'}, {'name': 'University of Southampton'}]}

