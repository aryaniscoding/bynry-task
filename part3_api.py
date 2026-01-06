from flask import Flask,jsonify
from sqlalchemy import text

@app.route('/api/companies/<int:company_id>/alersts/low-stock',methods = ['GET'])
def get_low_stock_alerts(company_id):
    #getting inventory list first 

    sql = text(f"""
        SELECT 
               p.id as pid, p.name, p.sku ,p.price,
               w.id as wid , w.name as w_name,
               i.quantity as stock,
               s.id as sid,s.name as sname ,s.email
        FROM inventory i
        JOIN products p on i.product_id = p.id
        JOIN warehouses w on i.warehouse_id = w.id
        left join supplier_products sp on p.id = sp.product_id
        left join supplier s on sp.supplier_id = s.id
        where w.company_id = {company_id}
    """)

    inventory_items = db.session.execute(sql)
    list_for_alerts = []

    for item in inventory_items:
        #1-selecting threshold manually 
        if item.price and item.price > 1000:
            threshold = 5 #high price items get a lower warn
        else :
            threshold = 20
        if item.stock >= threshold:
            continue
            #nothing needed as stock is adequate
        
        #2-checking recent sales
        sales_sql = text(f"""
            select sum(quantity) from sales_order_items s
            join sales_orders so on s.order_id = so.id
            where s.product_id = {item.pid}
            and so.created_at >= NOW() - INTERVAL '30 days' 
        """)
        
        recent_sales = db.session.execute(sales_sql).scalar() or 0

        if recent_sales == 0:
            continue
        #this is the dead stock which no one is buying hence we dont need to alert it

        avg_daily_sales = recent_sales/30.0
        days_left = int(item.stock/avg_daily_sales)

        #3 add everything to return listt
        list_for_alerts.append({
            "product_id" : item.pid,
            "product_name" : item.name,
            "sku" : item.sku,
            "warehouse_id" : item.wid,
            "warehouse_name" : item.w_name,
            "current_stock" : item.stock,
            "threshold" : threshold,
            "days_until_stockout":days_left,
            "supplier":{
                "id" : item.sid,
                "name":item.sname,
                "mobile":item.phone
                #i used phone number instead of email in data definition 
            }
        })
    return jsonify({
        "alerts":list_for_alerts,
        "total_alerts" : len(list_for_alerts)
    })

