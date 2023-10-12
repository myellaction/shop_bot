import asyncpg
from asyncpg import Connection
from data.config import DB_NAME, DB_PASS, DB_USER, DB_HOST

class Database:

    def __init__(self, pool):
        self.pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(user = DB_USER, password = DB_PASS,
                                         host = DB_HOST, database = DB_NAME)
        return cls(pool)

    async def execute(self, command, *args, fetch=False,
                      fetchval=False, fetchrow=False, execute=False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_tables(self):
        sql_category = 'CREATE TABLE IF NOT EXISTS category(category_id BIGSERIAL PRIMARY KEY,' \
                       ' category_name VARCHAR(100) NOT NULL);'
        sql_subcategory="CREATE TABLE IF NOT EXISTS subcategory(subcategory_id BIGSERIAL PRIMARY KEY," \
                        "subcategory_name VARCHAR(100) NOT NULL," \
                        "category_id BIGINT REFERENCES category(category_id) ON DELETE CASCADE " \
                        "ON UPDATE CASCADE);"
        sql_item = 'CREATE TABLE IF NOT EXISTS item(item_id BIGSERIAL PRIMARY KEY,' \
                   'item_name VARCHAR(200) NOT NULL,' \
                   'price DECIMAL(8,2), img VARCHAR(200),' \
                   'available BOOLEAN DEFAULT TRUE,' \
                   'category_id BIGINT REFERENCES category(category_id) ON DELETE CASCADE ON UPDATE CASCADE,' \
                   'subcategory_id BIGINT REFERENCES subcategory(subcategory_id) ON DELETE CASCADE ' \
                   'ON UPDATE CASCADE);'
        sql_buyer='CREATE TABLE IF NOT EXISTS buyer(buyer_id BIGINT PRIMARY KEY, ' \
                  'buyer_name VARCHAR(200), buyer_username VARCHAR(200));'

        sql_order_purchase = " CREATE TABLE IF NOT EXISTS order_purchase (order_purchase_id BIGSERIAL " \
                             "PRIMARY KEY," \
                             "total DECIMAL(8,2), status VARCHAR (60) DEFAULT 'Новый', " \
                             "delivery VARCHAR (60));"

        sql_order = "CREATE TABLE IF NOT EXISTS purchase (purchase_id BIGSERIAL PRIMARY KEY, " \
                    "buyer_id BIGINT REFERENCES buyer(buyer_id) ON DELETE CASCADE ON UPDATE CASCADE," \
                    "item_id BIGINT REFERENCES item(item_id) ON DELETE CASCADE ON UPDATE CASCADE," \
                    "amount INTEGER DEFAULT 0," \
                    " order_purchase_id BIGINT REFERENCES order_purchase(order_purchase_id) " \
                    "ON DELETE CASCADE ON UPDATE CASCADE);"


        command = sql_category + sql_subcategory + sql_item + sql_buyer + sql_order_purchase + sql_order
        return await self.execute(command, execute = True)


    async def drop_tables(self):
        sql = 'DROP TABLE IF EXISTS purchase, buyer, item, subcategory,' \
              'category, order_purchase CASCADE'
        return await self.execute(sql, execute=True)

    async def add_category(self,name):
        sql ='INSERT INTO category(category_name) VALUES($1)'
        return await self.execute(sql, name, execute=True)

    async def add_subcategory(self,name, category_id):
        sql ='INSERT INTO subcategory(category_id, subcategory_name) VALUES($1, $2)'
        return await self.execute(sql,category_id, name, execute=True)

    async def add_item(self,name,price,category_id, subcategory_id, img=None):
        sql ='INSERT INTO item(item_name, price, img, category_id, subcategory_id) ' \
             'VALUES($1, $2, $3, $4, $5)'
        return await self.execute(sql,name, price, img, category_id, subcategory_id, execute=True)

    async def get_cats(self):
        sql = 'SELECT * FROM category'
        res = await self.execute(sql, fetch=True)
        return res

    async def get_subcats(self, category_id=None):
        sql = 'SELECT * FROM subcategory'
        params=[]
        if category_id:
            sql = 'SELECT * FROM subcategory WHERE category_id = $1'
            params.append(category_id)
        res = await self.execute(sql,*params, fetch=True)
        return res

    async def get_items(self, category_id=None, subcategory_id=None):
        params = []
        if not category_id:
            sql = 'SELECT * FROM item'
        elif category_id and subcategory_id:
            sql = 'SELECT * FROM item WHERE category_id=$1 AND subcategory_id=$2'
            params = [category_id, subcategory_id]
        elif category_id:
            sql = 'SELECT * FROM item WHERE category_id = $1'
            params = [category_id]
        else:
            return None
        res = await self.execute(sql, *params, fetch=True)
        res = [dict(i) for i in res]
        return res

    async def get_item(self, item_id=None):
        sql = 'SELECT * FROM item WHERE item_id = $1'
        return await self.execute(sql, item_id, fetchrow=True)

    async def get_buyer(self, buyer_id=None):
        sql = 'SELECT * FROM buyer WHERE buyer_id = $1'
        return await self.execute(sql, buyer_id, fetchrow=True)

    async def add_buyer(self, buyer_id, buyer_name, buyer_username):
        sql = 'INSERT INTO buyer (buyer_id, buyer_name, buyer_username)' \
              'VALUES($1, $2, $3);'
        return await self.execute(sql, buyer_id, buyer_name, buyer_username, execute=True)

    async def delete_buyer(self,buyer_id):
        sql = 'DELETE FROM buyer WHERE buyer_id =$1'
        return await self.execute(sql, buyer_id, execute=True)

    async def add_purchase(self, buyer_id, item_id,amount=1):
        sql = 'INSERT INTO purchase(buyer_id,item_id,amount) VALUES ($1,$2,$3)'
        return await self.execute(sql, buyer_id, item_id, amount, execute=True)

    async def get_purchase(self, buyer_id=None, item_id=None,purchase_id=None):
        if not purchase_id:
            sql = 'SELECT * FROM purchase WHERE buyer_id = $1 AND item_id = $2 ' \
                  'AND amount >0 AND order_purchase_id IS NULL'
            return await self.execute(sql, buyer_id, item_id, fetchrow=True)
        else:
            sql = 'SELECT * FROM purchase WHERE purchase_id=$1 AND amount >0 ' \
                  'AND order_purchase_id IS NULL'
            return await self.execute(sql, purchase_id, fetchrow=True)

    async def get_purchases_by_order(self,order_purchase_id):
        sql = 'SELECT * FROM purchase WHERE order_purchase_id = $1 ORDER BY purchase_id'
        return await self.execute(sql, order_purchase_id,fetch=True)


    async def get_purchase_all(self, buyer_id):
        sql = 'SELECT * FROM purchase WHERE buyer_id = $1 AND amount > 0 ' \
              'AND order_purchase_id IS NULL ORDER BY purchase_id'
        return await self.execute(sql,buyer_id, fetch=True)


    async def edit_purchase(self, purchase_id, amount):
        sql = 'UPDATE purchase SET amount = $2 WHERE purchase_id = $1'
        return await self.execute(sql, purchase_id, amount, execute=True)

    async def delete_purchases_creating(self, buyer_id):
        sql = 'DELETE FROM purchase WHERE buyer_id = $1 AND order_purchase_id IS NULL;'
        return await self.execute(sql, buyer_id, execute=True)

    async def add_order_purchase(self, buyer_id, total, delivery):
        sql = 'INSERT INTO order_purchase (total, delivery) VALUES ($1, $2) RETURNING order_purchase_id;'
        order_purchase_id = (await self.execute(sql, total, delivery, fetchrow=True)).get('order_purchase_id')
        sql_delete_zero = 'DELETE FROM purchase WHERE buyer_id = $1 AND amount = 0'
        await self.execute(sql_delete_zero, buyer_id, execute=True)
        sql_edit_id = 'UPDATE purchase SET order_purchase_id = $1 WHERE buyer_id = $2 ' \
                      'AND order_purchase_id IS NULL;'
        await self.execute(sql_edit_id, order_purchase_id, buyer_id, execute=True)
        return order_purchase_id

    async def get_order_purchases(self, buyer_id, status):
        if not buyer_id:
            sql = "SELECT * FROM order_purchase WHERE status = $1 ORDER BY order_purchase_id DESC"
            return await self.execute(sql, status, fetch=True)

        if status == 'Все':
            sql = "SELECT DISTINCT order_purchase.order_purchase_id, total FROM purchase INNER JOIN order_purchase " \
              "ON purchase.order_purchase_id = order_purchase.order_purchase_id AND " \
              "purchase.buyer_id = $1 AND order_purchase.status IN ('Отменен', 'Доставленный') ORDER BY 1 DESC;"
        else:
            sql = "SELECT DISTINCT order_purchase.order_purchase_id, total FROM purchase INNER JOIN order_purchase " \
                  "ON purchase.order_purchase_id = order_purchase.order_purchase_id AND " \
                  "purchase.buyer_id = $1 AND status NOT IN ('Отменен', 'Доставленный') ORDER BY 1 DESC;"
        return await self.execute(sql, buyer_id, fetch=True)

    async def get_order_purchase(self, order_purchase_id):
        sql = 'SELECT * FROM order_purchase WHERE order_purchase_id = $1'
        return await self.execute(sql,order_purchase_id, fetchrow=True)

    async def edit_order_status_or_delete(self, order_purchase_id, action):
        if action == 'delete':
            sql = 'DELETE FROM order_purchase WHERE order_purchase_id =$1'
            return await self.execute(sql, order_purchase_id, execute = True)
        elif action == 'cancel':
            sql = "UPDATE order_purchase SET status = 'Отменен' WHERE order_purchase_id = $1"
            return await self.execute(sql, order_purchase_id, execute= True)
        else:
            sql = 'UPDATE order_purchase SET status = $1 WHERE order_purchase_id =$2'
            return await self.execute(sql, action, order_purchase_id, execute =True)







