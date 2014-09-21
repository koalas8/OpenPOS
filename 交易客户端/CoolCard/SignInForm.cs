using System;
using System.Collections.Generic;
using System.Collections;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Security.Cryptography;
using Newtonsoft.Json.Converters;
using CoolCard;

namespace CoolCard
{
    public partial class SignInForm : Form
    {
        public SignInForm()
        {
            InitializeComponent();
            this.ControlBox = false;
            this.ShowInTaskbar = false;
            this.KeyPreview = true;
        }

        private void SignInForm_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                String operator_no = this.textBox_operator_no.Text.Trim();
                String operator_password = this.textBox_operator_password.Text.Trim();
                if (operator_password == "")
                {
                    this.textBox_operator_password.Focus();
                    return;
                }
                if (operator_no == "")
                {
                    this.textBox_operator_no.Focus();
                    return;
                }

//                DB db = new DB();
//                String sql = "SELECT * FROM operators WHERE operator_no ='" + operator_no + "' AND password = '" + operator_password + "'";
//                SQLiteDataReader dr = db.ExecuteReturnSQL(sql);
//                if (dr == null)
//                {
//                    MessageBox.Show("未知错误,请联系软件提供商");
//                    return;
//                }
//                if (dr.HasRows == true)
//                {
                    //签到交易包
                    
                    MainForm.trans.init();
                    Config cfg = new Config();

                    MainForm.trans.Action = "singin";     
					MainForm.trans.Operator_Account = operator_no;
					MainForm.trans.Operator_Password = CoolCard.Security.MD5Encrypt(operator_password);
                    string transString = MainForm.trans.Build_Trans_String();

                    MySocket mSocket = new MySocket();
                    string rtnString = mSocket.Send(transString);

                    //处理返回结果
                    rtnString = rtnString.Replace(@"""", "").Replace("'", "").Replace("{", "").Replace("}", "");
                    string[] tmp_arr1 = rtnString.Split(',');
                    string[] tmp_arr2;
                    Hashtable hashTable = new Hashtable();
                    for (int i = 0; i < tmp_arr1.Length; i++)
                    {
                        tmp_arr2 = tmp_arr1[i].ToString().Split(':');
                        hashTable.Add(tmp_arr2[0].ToString(), tmp_arr2[1].ToString());
                    }
                    //如果返回成功，则更新本地数据表中的交易记录状态为"s"
                    string trans_date = "";
                    string trans_time = "";
                    string result_code = "";
                    int batch_no = 0;
                    int tracte_no = 0;
                    foreach (DictionaryEntry de in hashTable)
                    {
                        if (de.Key.ToString().Trim() == "result_code")
                        {
                            result_code = de.Value.ToString().Trim();
                        }
                        if (de.Key.ToString().Trim() == "trans_date")
                        {
                            trans_date = de.Value.ToString().Trim();
                        }
                        if (de.Key.ToString().Trim() == "trans_time")
                        {
                            trans_time = de.Value.ToString().Trim();
                        }
                        if (de.Key.ToString().Trim() == "batch_no")
                        { 
                            batch_no = Convert.ToInt32(de.Value.ToString());
                        }
                        if(de.Key.ToString().Trim() == "trace_no")
                        {
                            tracte_no = Convert.ToInt32(de.Value.ToString());
                        }
                    }

                    if (result_code == "0")
                    {
                        MainForm.login = true;
                        MainForm.current_operator = operator_no;
                        DB db = new DB();
                        db.ExecuteNoReturnSQL(String.Format("UPDATE settings SET val = '{0}' WHERE setting = 'current_batch_no'", batch_no.ToString()));
                        db.ExecuteNoReturnSQL(String.Format("UPDATE settings SET val = '{0}' WHERE setting = 'current_trace_no'", tracte_no.ToString()));
                        this.Close();
                    }
                    else
                    {
                        MessageBox.Show(result_code.ToString() + ":" + CoolCard .Config .GetConfig ("ERRORCODE", result_code, ""), "", MessageBoxButtons.OK, MessageBoxIcon.Error);                        
                    }
//                }
//                else
//                {
//                    MessageBox.Show("操作员不存在或密码错");
//                }
            }
            else if (e.KeyCode == Keys.Escape)
            {
                MainForm.loginCanceled = true;
                MainForm.login = true;
                this.Close();
            }
        }
    }
}