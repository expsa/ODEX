# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError


class IncomingOutgoingReport(models.AbstractModel):
    _name="report.stock_custom_reports.incoming_outgoing_prices_temp"



    @api.model
    def get_report_values(self,docids, data):
        date_from = data['data'][0]['date_from']
        date_to = data['data'][0]['date_to']
        location_id = data['data'][0]['location_id']
        conditions = " "
        products_names = ""
        category = ""
        if data['data'][0]['category_id']:

              category = data['data'][0]['category_id'][1]
              conditions = conditions +  " and prod_temp.categ_id=(%s)"%data['data'][0]['category_id'][0]

        if data['data'][0]['product_ids']:
              prod_obj = self.env['product.product']
              product = data['data'][0]['product_ids']
              if len(product) == 1:
                  products_names = prod_obj.browse(product).product_tmpl_id.name
                  conditions = conditions +  " and line.product_id = (%s)"%data['data'][0]['product_ids'][0]                  
              else:
                  for prod in product:
                      products_names = products_names  + prod_obj.browse(prod).product_tmpl_id.name + " "

                  conditions = conditions +  " and line.product_id in %s"%str(tuple(data['data'][0]['product_ids']))
        
        """ Get Opening Quantites """
          
        sql = """
                 CREATE OR REPLACE FUNCTION GetOpeinningInQty(ProductID int,location_id int,move_date date)  
                 RETURNS integer 
                 AS $$   
                 DECLARE 
                 prod_qty int;
                 prod_id int ; 

                 BEGIN
                 EXECUTE 'SELECT line.product_id as product, sum(line.qty_done) FROM stock_move_line line 
                          WHERE  line.location_dest_id = $1 and line.date < $2 and line.product_id = $3
                                 group by line.product_id' 
                                 INTO prod_id,prod_qty
                                 using location_id,move_date,ProductID;

                 IF (prod_qty IS NULL) then
                    prod_qty = 0;  
                    end if; 
                 RETURN prod_qty;  
                 END;
                 $$
                 LANGUAGE plpgsql;
                 CREATE OR REPLACE FUNCTION GetOpeinningOutQty(ProductID int,location_id int,move_date date)  
                 RETURNS integer 
                 AS $$   
                 DECLARE 
                 prod_qty int;
                 prod_id int ; 

                 BEGIN
                 EXECUTE 'SELECT line.product_id as product, sum(line.qty_done) FROM stock_move_line line 
                          WHERE  line.location_id = $1 and line.date < $2 and line.product_id = $3
                                 group by line.product_id' 
                                 INTO prod_id,prod_qty
                                 using location_id,move_date,ProductID;

                 IF (prod_qty IS NULL) then
                    prod_qty = 0;  
                    end if; 
                 RETURN prod_qty;  
                 END;
                 $$
                 LANGUAGE plpgsql;
                 CREATE OR REPLACE FUNCTION GetInQty(ProductID int,location_id int,from_date date,to_date date)  
                 RETURNS integer 
                 AS $$   
                 DECLARE 
                 prod_qty int;
                 prod_id int ; 

                 BEGIN
                 EXECUTE 'SELECT line.product_id as product, sum(line.qty_done) FROM stock_move_line line 
                          WHERE  line.location_dest_id = $1 and line.date >= $2 and line.date <= $4 and line.product_id = $3
                                 group by line.product_id' 
                                 INTO prod_id,prod_qty
                                 using location_id,from_date,ProductID,to_date;

                 IF (prod_qty IS NULL) then
                    prod_qty = 0;  
                    end if; 
                 RETURN prod_qty;  
                 END;
                 $$
                 LANGUAGE plpgsql;
                 CREATE OR REPLACE FUNCTION GetOutQty(ProductID int,location_id int,from_date date,to_date date)  
                 RETURNS integer 
                 AS $$   
                 DECLARE 
                 prod_qty int;
                 prod_id int ; 

                 BEGIN
                 EXECUTE 'SELECT line.product_id as product, sum(line.qty_done) FROM stock_move_line line 
                          WHERE  line.location_id = $1 and line.date >= $2 and line.date <= $4 and line.product_id = $3
                                 group by line.product_id' 
                                 INTO prod_id,prod_qty
                                 using location_id,from_date,ProductID,to_date;

                 IF (prod_qty IS NULL) then
                    prod_qty = 0;  
                    end if; 
                 RETURN prod_qty;  
                 END;
                 $$
                 LANGUAGE plpgsql;

                 select distinct prod_temp.name as product_name,line.product_id as product_id,GetOpeinningInQty(line.product_id,%s,'%s') AS open_inqty,GetOpeinningOutQty(line.product_id,%s,'%s') AS open_outqty,GetInQty(line.product_id,%s,'%s','%s') AS inqty,GetOutQty(line.product_id,%s,'%s','%s') AS outqty
                 from stock_move_line line
                 left join stock_move move on (line.move_id=move.id)
                 left join product_product prod on (line.product_id=prod.id)
                 left join product_template prod_temp on (prod.product_tmpl_id=prod_temp.id)
                 left join product_category cat on (prod_temp.categ_id=cat.id)

                 where  line.state = 'done' """%(location_id[0],date_from,location_id[0],date_from,location_id[0],date_from,date_to,location_id[0],date_from,date_to,) 
        sql = sql + conditions + "group by line.product_id,prod_temp.name order by line.product_id asc;"
        self._cr.execute(sql)
        res = self.env.cr.dictfetchall()
        for dic in res:
            dic['uom'] = self.env['product.product'].browse(dic['product_id']).product_tmpl_id.uom_id.name      
            dic['cost_price'] = self.env['product.product'].browse(dic['product_id']).product_tmpl_id.standard_price  
            dic['default_code'] = self.env['product.product'].browse(dic['product_id']).product_tmpl_id.default_code    

        docargs={
                'doc_ids':[],
                'doc_model':['stock.move.line'],
                'docs': res,	
                'date_from':data['data'][0]['date_from'],
                'date_to':data['data'][0]['date_to'],
                'location_id': location_id[1],
                'category' : category,
                'product_ids': products_names,
                'company':self.env.user.company_id,
                    }
        return docargs



