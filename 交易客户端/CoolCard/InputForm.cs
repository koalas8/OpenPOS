using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows.Forms;

namespace CoolCard
{
    public partial class InputForm : Form
    {
        private String inputType = "";　//输入类型
        private String amount = "";     //输入的金额
        private string newpassword = "";//卡改密交易中输入的新密码
        private string repassword = ""; //卡改密交易中输入的重复新密码
        private string Password="";     //交易中输入的卡密码
        private string date = "";   
        private string point = "";
        private string batch_no = "";
        private string trace_no = "";

        /// <summary>
        /// 判断按下键是否是数字键
        /// </summary>
        /// <param name="e">键盘事件</param>
        /// <returns>true OR false</returns>
        private bool isKeyInNumRange(KeyEventArgs e) {
            if ((e.KeyValue >= 48 && e.KeyValue <= 57) || (e.KeyValue >= 96 && e.KeyValue <= 105))
            {
                return true;
            }
            else 
            {
                return false;
            }
        }

        private string getNumKeyFace(KeyEventArgs e)
        {
            int keyNum = 0;
            keyNum = (int)e.KeyValue;
            if (keyNum >= 48 && keyNum <= 57)
            {
                keyNum = keyNum - 48;
            }
            else if(e.KeyValue >= 96 && e.KeyValue <= 105) 
            {
                keyNum = keyNum - 96;
            }
            return keyNum.ToString();
        }

        public String InputType
        { 
            set 
            {
                inputType = value;

                if ("newpassword" == value.ToLower())
                {
                    this.label1.Text = "请输入新密码";
                    this.textBox1.PasswordChar = '*';
                    this.textBox1.Text = "";
                    this.textBox1.MaxLength = 10;
                    this.textBox1.ReadOnly = true;
                }
                else if ("repassword" == value.ToLower())
                {
                    this.label1.Text = "请再输入一遍密码";
                    this.textBox1.PasswordChar = '*';
                    this.textBox1.Text = "";
                    this.textBox1.MaxLength = 10;
                    this.textBox1.ReadOnly = true;
                }
                else if ("masterpassword" == value.ToLower())
                {
                    this.label1.Text = "请输入主管密码";
                    this.textBox1.PasswordChar = '*';
                    this.textBox1.Text = "";
                    this.textBox1.MaxLength = 6;
                    this.textBox1.ReadOnly = true;
                }
                else if ("password" == value.ToLower())
                {
                    this.label1.Text = "请输入密码";
                    this.textBox1.PasswordChar = '*';
                    this.textBox1.Text = "";
                    this.textBox1.MaxLength = 10;
                    this.textBox1.Enabled = false ;
                }                
                else if ("card" == value.ToLower())
                {
                    this.label1.Text = "请刷卡";
                    this.textBox1.MaxLength = 37;
                    this.textBox1.Text = "";
                    this.textBox1.ReadOnly = false;
                    //CoolCard.MagneticCollector collector = new MagneticCollector();
                    //this.textBox1.Text = collector.getTrack1(); 
                }
                else if ("amount" == value.ToLower())
                {
                    this.label1.Text = "请输入金额";
                    this.textBox1.Text = "";
                    this.textBox1.Text = "0.00";
                    this.textBox1.ReadOnly = true;
                }
                else if ("date" == value.ToLower())
                {
                    this.textBox1.ReadOnly = true;
                    this.label1.Text = "请输入日期(YYYYMMDD)";
                    this.textBox1.Text = "";
                }
                else if ("point" == value.ToLower())
                {
                    this.label1.Text = "请输入积分";
                    this.textBox1.Text = "";
                    this.textBox1.ReadOnly = true;
                }
                else if ("batch_no" == value.ToLower()) 
                {
                    this.textBox1.ReadOnly = true;
                    this.label1.Text = "请输入交易批次号";
                    this.textBox1.Text = "";
                    
                }
                else if ("trace_no" == value.ToLower())
                {
                    this.textBox1.ReadOnly = true;
                    this.label1.Text = "请输入交易流水号";
                    this.textBox1.Text = "";
                }
                else if ("deposit" == value.ToLower())
                {
                    this.label1.Text = "请输入充值金额";
                    this.textBox1.Text = "";
                    this.textBox1.ReadOnly = true;
                }
            }
        }
        public InputForm()
        {
            InitializeComponent();
            this.KeyPreview = true;
            this.ControlBox = false;
            this.InitPara();
        }

        private void InitPara()
        {
            this.Password = "";
            this.repassword = "";
            this.newpassword = "";
            this.point = "";
            this.amount = "";
            this.date = "";
            this.trace_no = "";
        }

        private void InputForm_KeyDown(object sender, KeyEventArgs e)
        {            
            Config cfg = new Config();
            if (e.KeyValue.ToString() == cfg.getCancelKeyValue()) //按下了交易取消键
            {
                MainForm.trans .Is_Canceled = true;
                this.InitPara();
                this.Close();               
            }

            //根据不同的输入类型来进行不同的操作
            switch (inputType) { 
                case "password": //密码
                    if (e.KeyCode == Keys.Enter)
                    {
                        MainForm.trans.Password = this.textBox1.Text.Trim();
                        this.Close();
                    }
                    else if(this.isKeyInNumRange(e)  && this.textBox1 .Text .Length < 20)
                    {
                        this.Password += this.getNumKeyFace(e);
                        this.textBox1.Text =this.Password;
                    }
                    break;
                case "newpassword": //新密码
                    if (e.KeyCode == Keys.Enter)
                    {
                        MainForm.newPasswrod = this.textBox1.Text.Trim();
                        this.Close();
                    }
                    else if(this.isKeyInNumRange(e)  && this.textBox1 .Text .Length < 20)
                    {
                        this.newpassword += this.getNumKeyFace(e);
                        this.textBox1.Text = this.newpassword;
                    }
                    break;
                case "repassword": //重新输入一遍密码
                    if (e.KeyCode == Keys.Enter)
                    {
                        MainForm.rePasswrod = this.textBox1.Text.Trim();
                        this.Close();
                    }
                    else if(this.isKeyInNumRange (e)  && this.textBox1 .Text .Length < 20)
                    {
                        this.repassword += this.getNumKeyFace(e);
                        this.textBox1.Text = this.repassword;
                    }
                    break;
                case "card": //刷卡
                    if (e.KeyCode == Keys.Enter)
                    {
                        if (this.textBox1.Text.Trim().Length == 18) //输入的卡号需是18位
                        {
                            MainForm.trans.Card_No = this.textBox1.Text.Trim();
                            this.Close();
                        }
                    }
                    break;
                case "batch_no": // 批次号输入
                    if (this.isKeyInNumRange(e))
                    {
                        this.batch_no += this.getNumKeyFace(e);
                        this.textBox1.Text = this.batch_no;
                    }
                    else if (e.KeyCode == Keys.Enter)
                    {
                        MainForm.trans.Old_Batch_No = this.textBox1.Text.Trim();
                        this.Close();
                    }
                    break;
                case "trace_no": //流水号输入
                    if (this.isKeyInNumRange(e) && this.textBox1 .Text .Length < 20)
                    {
                        this.trace_no += this.getNumKeyFace(e);
                        this.textBox1.Text = this.trace_no;
                    }
                    else if (e.KeyCode == Keys.Enter)
                    { 
                        MainForm.trans.Old_Trace_No = this.textBox1 .Text .Trim ();
                        this.Close();
                    }
                    break;
                case "point": //积分输入
                    if (this.textBox1.Text.Trim() == "")
                    {  //第一个输入的字符不能是"0"
                        if (e.KeyValue >= 97 && e.KeyValue <= 105)
                        {
                            this.point += this.getNumKeyFace(e);
                            this.textBox1.Text = this.point;
                        }
                    }
                    else
                    {
                        if (this.isKeyInNumRange(e))
                        {
                            this.point += this.getNumKeyFace(e);
                            this.textBox1.Text = this.point;
                        }
                    }
                    if (e.KeyCode == Keys.Enter)
                    {
                        if (this.textBox1.Text.Trim() != "")
                        {
                            MainForm.trans.Amount = this.textBox1.Text.Trim();
                            this.Close();
                        }
                    }
                    break;
                case "amount": //金额输入
                    if (e.KeyCode == Keys.Enter)
                    {
                        if (this.textBox1.Text.Trim() != "0.00")
                        {
                            MainForm.trans.Amount = amount;
                            this.Close();
                        }
                    }
                    else if (this.isKeyInNumRange(e))
                    {
                        amount = amount + this.getNumKeyFace(e);
                        //amount  = amount.Replace(".", "").ToLower().Replace("numpad", "").Trim();
                        //检查money是否以"0"开头,如果允许以"0"开头的话则会出现"000000.00"格式的金额
                        if (amount.Substring(0, 1).ToString() == "0")
                        {
                            amount = amount.Substring(1, amount.Length - 1);
                        }
                        //每输入一个数字则清空一次输入框，并赋予其新的金额数值
                        switch (amount.Trim().Length)
                        {
                            case 0:
                                this.textBox1.Text = "0.00";
                                break;
                            case 1:
                                this.textBox1.Text = "0.0" + amount;
                                break;
                            case 2:
                                this.textBox1.Text = "0." + amount;
                                break;
                            default:
                                this.textBox1.Text = amount.Insert(amount.Length - 2, ".");
                                break;
                        }
                    }
                    break;
                case "date": //日期输入
                    if (e.KeyCode == Keys.Enter)
                    {
                        if (this.textBox1.Text.Trim().Length != 8) //长度不为8则格式不正确
                        {
                            return;
                        }
                        else
                        {
                            if (!IsDate(this.textBox1.Text.Trim().Insert(4, "-").Insert(7, "-"))) //不符合日期格式不正确
                            {
                                return;
                            }
                            else
                            {
                                MainForm.trans.Overdue_Date = this.textBox1.Text.Trim();
                                this.Close();
                            }
                        }
                    }
                    else if (this.isKeyInNumRange(e)) 
                    {
                        this.date += this.getNumKeyFace(e);
                        this.textBox1.Text = this.date;
                    }
                    break;
            }
        }

        public static bool IsDate(string StrSource)
        {
            try
            {
                DateTime.Parse(StrSource).ToString("yyyyMMdd");
                return true;
            }
            catch 
            {
                return false;
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            if (this.textBox1.Text.Trim().Length == 34) {
                MainForm.trans.Track_2 = this.textBox1.Text.Trim();
                this.textBox1.Text = this.textBox1.Text.Trim().Substring(0, 18);                
            }
        }
    }
}