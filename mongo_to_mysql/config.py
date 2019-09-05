
# Mongo configuration
MONGO_DB = 'db-bd'


# Global Config
METADATA_RELATION_TABLE = "CREATE TABLE IF NOT EXISTS migration_metadata_ration_table ( " \
                          "id INT NOT NULL AUTO_INCREMENT, " \
                          "primary_t VARCHAR(500) NOT NULL, " \
                          "secondary_t VARCHAR(500) NOT NULL, " \
                          "relation VARCHAR(200) not null, " \
                          "PRIMARY KEY (id)" \
                          ");"
