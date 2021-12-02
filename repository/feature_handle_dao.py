import repository


class FeatureHandleDao(repository.MySQLRepository):
    def feature_search(self, table_name: str, column_name: str, connection_feature):
        sql = """select distinct(%s) from %s""" % (column_name, table_name)
        with connection_feature.cursor() as cursor:
            cursor.execute(sql)
        feature_list = cursor.fetchall()
        return feature_list


class FeatureHandleDaoMongo():
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    def _set_collection(self, collection_name: str):
        self.collection = self.mongo_client[collection_name]

    def feature_search_mongo(self, column_name: str):
        column_name = '$' + "%s" % column_name
        pipeline = [{'$group': {'_id': column_name}}]
        cursor = self.collection.aggregate(pipeline)
        data = list(cursor)
        column_value = {}
        feature_list = []
        for i in range(0, len(data)):
            column_value = {column_name: data[i]['_id']}
            feature_list.append(column_value)
        return feature_list
