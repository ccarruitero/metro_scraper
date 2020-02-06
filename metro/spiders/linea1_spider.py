# -*- coding: utf-8 -*-
import scrapy
import json


class Linea1Spider(scrapy.Spider):
    name = 'linea1'
    start_urls = ['https://www.lineauno.pe/horarios/']

    def parse(self, response):
        schedule_types = ['lunes-viernes'] # , 'sabados', 'domingos-feriados']
        for station_link in response.css('.estacion'):
            station = station_link.attrib['href'].split('/')[-1]
            for schedule_type in schedule_types:
                url = f'{response.request.url}{schedule_type}/{station}/'
                yield scrapy.http.Request(url, meta={'station': station, 'schedule_type': schedule_type}, callback=self.parse_schedule)

    def parse_schedule(self, response):
        schedules = response.css('carrusel-horarios')
        data = response.meta
        data['schedules'] = []
        for schedule in schedules:
            data['schedules'].extend(json.loads(schedule.attrib[':datos'])['array'])

        yield data
