from decimal import Decimal
@app.route('/api/products' , methods = ['POST'])
def create_product():
    data = request.json

    try : 
        name = data['name']
        sku = data['sku']
        price = Decimal(str(data['price']))
        qty = int(data.get('initial_quantity' , 0)) #defaulting 0
        warehouse_id = data.get('warehouse_id')

        if price < 0 or qty < 0:
            return {"error": "Price/Quantity cannot be negative"}, 400
        
        product = Product(
            name = name,
            sku = sku,
            price = price
            #removing the warehouse_id
        )
        db.session.add(product)
        db.session.flush() #temp addition to db ,not commited

        if warehouse_id:
            inv = Inventory(
                product_id = product.id,
                warehouse_id = warehouse_id,
                quantity = qty
            )
            db.session.add(inv)

        #finally commiting
        db.session.commit()
        return {"message": "Success", "product_id": product.id}, 201
    except KeyError:
        db.session.rollback()
        return {"error": "Missing name, sku, or price"}, 400
    except Exception:
        db.session.rollback()
        return {"error": "Invalid data format"}, 400