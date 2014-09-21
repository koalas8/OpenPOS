using System;
using System.Collections.Generic;
using System.Text;
using System.Data.OleDb;
using System.Data.SqlClient;
using System.Data;

namespace CoolCard
{
    class DB
    {
        private OleDbConnection conn = new OleDbConnection(@"Provider=Microsoft.Jet.OLEDB.4.0; Data Source=CoolCard.mdb");
        //打开连接
        public void OpenConnection()
        {
            if (conn.State == System.Data.ConnectionState.Closed)
            {
                this.conn.Open();
            }
        }

        //关闭连接
        public void CloseConnection()
        {
            if (conn.State == System.Data.ConnectionState.Open)
            {
                this.conn.Close();
            }
        }

        public int GetCount(String sql)
        {
            DataTable dt = new DataTable();
            dt = this.ExecuteReturnSQL(sql);
            return Convert.ToInt32(dt.Rows[0][0].ToString());
        }

        //执行没有返回值SQL
        public bool ExecuteNoReturnSQL(String sql)
        {
            try{                
                this.OpenConnection();
                OleDbCommand comm = new OleDbCommand();
                comm.Connection = this.conn;
                comm.CommandType = System.Data.CommandType.Text;
                comm.CommandText = sql;
                comm.ExecuteNonQuery ();                
                return true;
            }catch(Exception e) {
                return false;
            }
        }

        //执行有返回的SQL
        public DataTable  ExecuteReturnSQL(String sql)
        {
            this.OpenConnection();
            OleDbDataAdapter da = new OleDbDataAdapter(sql, this.conn);
            DataTable dt = new DataTable();
            da.Fill(dt);
            return dt;
        }

        // 添加交易记录
        public void AddTrans(string id, string cardNo, string action, string batchNo, string traceNo, string amount, string Operator)
        {           
            string sql = String.Format("INSERT INTO trans(id, card_no, trans_name, amount, operator_no) VALUES('{0}', '{1}', '{2}', '{3}', '{4}')", id, cardNo, action, amount, Operator);
            this.ExecuteNoReturnSQL(sql);
        }

        // 更新交易记录
        public void UpdateTrans(string id, string transDate, string transTime, string batchNo, string traceNo, string state)
        {            
            string sql = String.Format("UPDATE trans SET trans_date='{0}', trans_time='{1}', batch_no='{2}', trace_no='{3}', state='{4}' WHERE id='{5}'", transDate, transTime, batchNo, traceNo, state, id);
            this.ExecuteNoReturnSQL(sql);
        }

    }
}
