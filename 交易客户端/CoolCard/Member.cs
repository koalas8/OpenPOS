using System;
using System.Collections.Generic;
using System.Text;
using System.Collections;

namespace CoolCard
{
    public class Member
    {
        /*
         *  会员信息
         */
        private String _member_name; //会员姓名
        private String _member_sex;  //会员性别 
        private String _member_id_number;   //会员证件号码
        private String _member_card_number;  //会员卡号
        private String _member_cell_number; //会员手机号码
        private String _member_remark;      //会员备注信息
        private String _action;

        public String Action
        {
            get { return _action; }
            set { _action = value; }
        }

        public String Member_Name
        {
            get { return _member_name; }
            set { _member_name = value; }
        }

        public String Member_Sex
        {
            get { return _member_sex; }
            set { _member_sex = value; }
        }

        public String Member_Id_Number
        {
            get { return _member_id_number; }
            set { _member_id_number = value; }
        }

        public String Member_Card_Number
        {
            get { return _member_card_number; }
            set { _member_card_number = value; }
        }

        public String Member_Cell_Number
        {
            get { return _member_cell_number; }
            set { _member_cell_number = value; }
        }
        public String Member_Remark
        {
            get { return _member_remark; }
            set { _member_remark = value; }
        }

        public void init()
        {
            this.Action = "";
            this.Member_Cell_Number = "";
            this.Member_Id_Number = "";
            this.Member_Name = "";
            this.Member_Remark = "";
            this.Member_Sex = "";
            this.Member_Card_Number = "";
        }

        public String Build_String()
        {
            /* 生成交易字符串 */

            Hashtable ht = new Hashtable();
            ht.Add("action", this.Action);
            ht.Add("Member_Phone_Number", this.Member_Cell_Number );
            ht.Add("Member_Id_Number", this.Member_Id_Number);
            ht.Add("Member_Name", this.Member_Name);
            ht.Add("Member_Remark", this.Member_Remark );
            ht.Add("Member_Sex",this.Member_Sex);
            ht.Add("Member_Card_Number", this.Member_Card_Number);

            String trans_string = "";
            foreach (DictionaryEntry de in ht)
            {
                //if (de.Value.ToString().Trim() != "") 
                //{
                trans_string += ("'" + de.Key.ToString().ToLower() + "':'" + de.Value.ToString().ToLower() + "',");
                //}
            }
            trans_string = trans_string.Substring(0, trans_string.Length - 1);
            trans_string = "{" + trans_string + "}";

            return trans_string;
        }
    }
}
