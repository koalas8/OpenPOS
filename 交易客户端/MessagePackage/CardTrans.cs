using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace CoolCard
{
    namespace MessagePackage
    {
        public class CardTrans
        {
            /*
            *  卡交易信息
            */
            private String _oper_account;	// 收银员账号       
            private String _oper_pass;		// 收银员密码
            private String _action;         // 交易类型
            private String _Trans_Time;     // 交易时间
            private String _Trans_Date;     // 交易日期
            private String _Shop_No;        // 商户号
            private String _Terminal_No;    // 终端号
            private String _Card_No;        // 交易卡号
            private String _track_2;        // 第二磁道
            private String _password;       // 持卡人密码
            private String _new_password;   // 新密码
            private String _renew_password; // 再输入的新密码
            private String _master_password;// 主管密码
            private String _amount;         // 交易金额(单位:分)
            private String _Current_Points; // 本次积分
            private String _Total_Points;   // 总积分
            private String _Batch_No;       // 批次号
            private String _Trace_No;       // 流水号
            private String _Old_Batch_No;   // 原批次号(用于撤销交易和退货交易)
            private String _Old_Trace_No;   // 原流水号(用于撤销交易和退货交易)
            private String _result;         // 交易结果 
            private String _overdue_date;   // 有效期
            private String _payment_count;  // 消费笔数(用于结算)
            private String _payment_amount; // 消费金额(用于结算)
            private String _deposit_count;  // 充值笔数(用于结算)
            private String _deposit_amount; // 充值金额(用于结算)
            private String _points_payment_count;   // 积分消费笔数(用于结算)
            private String _points_payment_amount;  // 积分消费金额(用于结算)
            private String _points_deposit_count;   // 积分充值笔数(用于结算)
            private String _points_deposit_amount;  // 积分充值金额(用于结算)
            private bool _is_canceled;      // 交易是否取消
            private String _key;            // 工作密钥

            public String Operator_Account{
                get { return _oper_account; }
                set { _oper_account = value; }
            }

            public String Operator_Password
            {
                get { return _oper_pass; }
                set { _oper_pass = value; }
            }

            public String Action
            {
                get { return _action; }
                set { _action = value; }
            }

            public String Trans_Time
            {
                set { _Trans_Time = value; }
                get { return _Trans_Time; }
            }

            public String Trans_Date
            {
                set { _Trans_Date = value; }
                get { return _Trans_Date; }
            }

            public String Shop_No
            {
                set { _Shop_No = value; }
                get { return _Shop_No; }
            }

            public String Terminal_No
            {
                set { _Terminal_No = value; }
                get { return _Terminal_No; }
            }

            public String Card_No
            {
                set { _Card_No = value; }
                get { return _Card_No; }
            }

            public String Track_2
            {
                set { _track_2 = value; }
                get { return _track_2; }
            }

            public String Password
            {
                set { _password = value; }
                get { return _password; }
            }

            public String NewPassword
            {
                get { return _new_password; }
                set { _new_password = value; }
            }

            public String ReNewPassword
            {
                get { return _renew_password; }
                set { _renew_password = value; }
            }

            public String MasterPassword
            {
                get { return _master_password; }
                set { _master_password = value; }
            }

            public String Amount
            {
                set { _amount = value; }
                get { return _amount; }
            }

            public String Current_Points
            {
                set { _Current_Points = value; }
                get { return _Current_Points; }
            }

            public String Total_Points
            {
                set { _Total_Points = value; }
                get { return _Total_Points; }
            }

            public String Batch_No
            {
                set { _Batch_No = value; }
                get { return _Batch_No; }
            }

            public String Trace_No
            {
                set { _Trace_No = value; }
                get { return _Trace_No; }
            }

            public String Old_Batch_No
            {
                set { _Old_Batch_No = value; }
                get { return _Old_Batch_No; }
            }

            public String Old_Trace_No
            {
                set { _Old_Trace_No = value; }
                get { return _Old_Trace_No; }
            }

            public String Result
            {
                set { _result = value; }
                get { return _result; }
            }

            public String Overdue_Date
            {
                set { _overdue_date = value; }
                get { return _overdue_date; }
            }

            public bool Is_Canceled
            {
                set { _is_canceled = value; }
                get { return _is_canceled; }
            }

            public String Key
            {
                set { _key = value; }
                get { return _key; }
            }

            public String Payment_Count
            {
                set { _payment_count = value; }
                get { return _payment_count; }
            }

            public String Payment_Amount
            {
                set { _payment_amount = value; }
                get { return _payment_amount; }
            }

            public String Deposit_Count
            {
                set { _deposit_count = value; }
                get { return _deposit_count; }
            }

            public String Deposit_Amount
            {
                set { _deposit_amount = value; }
                get { return _deposit_amount; }
            }

            public String Points_Payment_Count
            {
                set { _points_payment_count = value; }
                get { return _points_payment_count; }
            }

            public String Points_Payment_Amount
            {
                set { _points_payment_amount = value; }
                get { return _points_payment_amount; }
            }

            public String Points_Deposit_Count
            {
                set { _points_deposit_count = value; }
                get { return _points_deposit_count; }
            }

            public String Points_Deposit_Amount
            {
                set { _points_deposit_amount = value; }
                get { return _points_deposit_amount; }
            }


            public void init()
            {
                /* 初始化类属性 */

                this.Action = "";
                this.Operator_Account = "";
                this.Operator_Password = "";
                this.Trans_Date = "";
                this.Trans_Time = "";

                DogReader dogReader = new DogReader();
                this.Key = dogReader.readDesKey();
                this.Shop_No = dogReader.readShopNo();
                this.Terminal_No = dogReader.readTerminalNo();

                this.Card_No = "";
                this.Track_2 = "";
                this.Password = "";
                this.NewPassword = "";
                this.ReNewPassword = "";
                this.MasterPassword = "";
                this.Amount = "";
                this.Current_Points = "";
                this.Total_Points = "";
                this.Batch_No = "";
                this.Trace_No = "";
                this.Old_Batch_No = "";
                this.Old_Trace_No = "";
                this.Payment_Count = "";
                this.Payment_Amount = "";
                this.Deposit_Count = "";
                this.Deposit_Amount = "";
                this.Points_Payment_Count = "";
                this.Points_Payment_Amount = "";
                this.Points_Deposit_Count = "";
                this.Points_Deposit_Amount = "";

                this.Result = "";
                this.Overdue_Date = "";
                this.Is_Canceled = false;
            }

            /// <summary>
            /// 生成交易包
            /// </summary>
            /// <returns>DES加密的数据包+未加密的终端号</returns>
            public String Build_Trans_String()
            {
                Hashtable ht = new Hashtable();
                ht.Add("Operator_Account", this.Operator_Account);
                ht.Add("Operator_Password", this.Operator_Password);
                ht.Add("action", this.Action);
                ht.Add("Trans_Time", this.Trans_Time);
                ht.Add("Trans_Date", this.Trans_Date);
                ht.Add("Shop_No", this.Shop_No);
                ht.Add("Terminal_No", this.Terminal_No);
                ht.Add("Card_No", this.Card_No);
                ht.Add("track_2", this.Track_2);
                ht.Add("password", this.Password);
                ht.Add("new_password", this.NewPassword);
                ht.Add("renew_password", this.ReNewPassword);
                ht.Add("master_password", this.MasterPassword);
                ht.Add("amount", this.Amount);
                ht.Add("Current_Points", this.Current_Points);
                ht.Add("Total_Points", this.Total_Points);
                ht.Add("Batch_No", this.Batch_No);
                ht.Add("Trace_No", this.Trace_No);
                ht.Add("Old_Batch_No", this.Old_Batch_No);
                ht.Add("Old_Trace_No", this.Old_Trace_No);
                ht.Add("Payment_Count", this.Payment_Count);
                ht.Add("Payment_Amount", this.Payment_Amount);
                ht.Add("Deposit_Count", this.Deposit_Count);
                ht.Add("Deposit_Amount", this.Deposit_Amount);
                ht.Add("Points_Payment_Count", this.Points_Payment_Count);
                ht.Add("Points_Payment_Amount", this.Points_Payment_Amount);
                ht.Add("Points_Deposit_Count", this.Points_Deposit_Count);
                ht.Add("Points_Deposit_Amount", this.Points_Deposit_Amount);
                ht.Add("Overdue_date", this.Overdue_Date);
                ht.Add("client_version", "1.0");

                String trans_string = "";
                foreach (DictionaryEntry de in ht)
                {
                    //if (de.Value.ToString().Trim() != "") 
                    //{                
                    trans_string += ("'" + de.Key.ToString().ToLower() + "':'" + de.Value.ToString() + "',");
                    //}
                }
                trans_string = trans_string.Substring(0, trans_string.Length - 1);
                trans_string = "{" + trans_string + "}";

                CoolCard.Security security = new Security();
                return (security.DESEncrypt(trans_string, this.Key) + this.Terminal_No);
            }

            public Hashtable GetReturnPackage(string rtnString)
            {
                rtnString = rtnString.Replace(@"""", "").Replace("'", "").Replace("{", "").Replace("}", "");
                string[] tmp_arr1 = rtnString.Split(',');
                string[] tmp_arr2;
                Hashtable hashTable = new Hashtable();
                for (int i = 0; i < tmp_arr1.Length; i++)
                {
                    tmp_arr2 = tmp_arr1[i].ToString().Split(':');
                    hashTable.Add(tmp_arr2[0].ToString(), tmp_arr2[1].ToString());
                }
                return hashTable;
            }
        }
    }
}
