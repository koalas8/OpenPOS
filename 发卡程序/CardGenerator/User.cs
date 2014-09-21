using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Data;
using CardGenerator;

namespace CardGenerator
{
    public class User
    {
        public static Boolean login(String userno, String password)
        {
            DB db = new DB();            
            long count = db.GetCount(String.Format("SELECT COUNT(*) FROM user_info WHERE user_no='{0}' AND password='{1}'", userno, Utils.md5(password)));
            if(count == 1)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
    }
}
