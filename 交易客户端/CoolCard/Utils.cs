using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Data;

namespace CoolCard
{
    class Utils
    {
        public static String getBatchNum()
        {
            DB db = new DB();
            DataTable batchData = db.ExecuteReturnSQL("SELECT val FROM settings WHERE setting = 'current_batch_no'");
            if (batchData.Rows.Count > 0)
            {
                String batchNum = batchData.Rows[0][0].ToString();
                return Convert.ToString(batchNum);
            }
            else
            { 
                return "1";
            }
             
        }

        public static String getTraceNum()
        { 
            DB db = new DB();
            DataTable traceData = db.ExecuteReturnSQL("SELECT val FROM settings WHERE setting = 'current_trace_no'");
            if (traceData.Rows.Count > 0)
            {
                String traceNum = traceData.Rows[0][0].ToString() ;
                return Convert.ToString(traceNum);
            }
            else
            {
                return "1";
            }
        }
    }
}
