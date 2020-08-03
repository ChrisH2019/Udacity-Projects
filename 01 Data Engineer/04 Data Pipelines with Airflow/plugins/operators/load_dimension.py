from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    truncate_sql = """
        TRUNCATE TABLE {}
    """
    insert_sql = """
        INSERT INTO {}
        {}
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_stmt="",
                 truncate_table=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_stmt = sql_stmt
        self.truncate_table = truncate_table

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.truncate_table:
            self.log.info(f"Truncating table {self.table}")
            formatted_sql = LoadDimensionOperator.truncate_sql.format(self.table)
            redshift.run(formatted_sql)
            
        self.log.info(f"Loading table {self.table}")
        formatted_sql = LoadDimensionOperator.insert_sql.format(
            self.table, 
            self.sql_stmt
        )
        redshift.run(formatted_sql)
        self.log.info(f"Done loading table {self.table}")
