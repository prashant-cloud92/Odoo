from odoo import models, fields, api
import base64
import csv
from io import StringIO
import time

class StudentImport(models.Model):
    _name = 'student.import'

    file=fields.Binary("csv file")
    file_name=fields.Char()


    def action_import_csv(self):
        csv_data = base64.b64decode(self.file)

        file_data = StringIO(
            csv_data.decode('utf-8')
        )

        reader = csv.DictReader(file_data)
        val_list=[]
        errors=[]

        for line_no, row in enumerate(reader,start=2):
            try:
                mob_no=row.get('contact_no')
                if not row.get('student_name'):
                    raise ValueError('Student Name Error')
                if len(mob_no)!=10:
                    raise ValueError('Contact Number Error')


                val_list.append({"name":row.get('student_name'),"email":row.get('email'),"contact_no":row.get('contact_no')})
            except Exception as e:
                errors.append(f"{line_no}: {e}")
                continue
        if val_list:
            start = time.time()

            self.env['student.data'].create(val_list)


            end = time.time()
            print(f"Time: {end - start:.2f} seconds")
        print(errors)




# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class csv_import(models.Model):
#     _name = 'csv_import.csv_import'
#     _description = 'csv_import.csv_import'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

