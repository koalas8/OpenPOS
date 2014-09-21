using System;
using System.Data;
using Npgsql;

namespace CardGenerator
{
    class DB
    {
        private const String ConnString = "Server=127.0.0.1;Port=5432;User Id=postgres;Password=123456;Database=jf_card;";
        public NpgsqlConnection Conn = new NpgsqlConnection(ConnString);

        /// <summary>
        /// 执行UPDATE, INSERT, DELETE语句
        /// </summary>
        /// <param name="sql"></param>
        /// <returns></returns>
        public Boolean ExecSql(String sql) 
        {
            if (Conn.State == ConnectionState.Closed)
            {
                Conn.Open();
            }
            var command = new NpgsqlCommand(sql, Conn);
            command.ExecuteNonQuery();
            return true;
        }

        /// <summary>
        /// 执行SELECT COUNT(*)语句
        /// </summary>
        /// <param name="sql"></param>
        /// <returns></returns>
        public long GetCount(String sql)
        {
            if(Conn.State ==  ConnectionState.Closed)
            {
                Conn.Open();
            }
            var command = new NpgsqlCommand(sql, Conn);
            var count = (long) command.ExecuteScalar();
            return count;
        }

        /// <summary>
        /// 执行SELECT语句
        /// </summary>
        /// <param name="sql"></param>
        /// <returns></returns>
        public DataTable GetData(String sql)
        {
            var datatable = new DataTable();
            var adapter = new NpgsqlDataAdapter(sql, Conn);
            adapter.Fill(datatable);
            return datatable;
        }
    }
}
