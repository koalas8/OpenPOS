using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using CoolCard;
using System.Threading;

namespace CoolCard
{
    public partial class MainForm : Form
    {
         
        public static MessagePackage.CardTrans trans = new MessagePackage.CardTrans();   // 交易
        public static string masterPassword = "";  // 主管密码
        public static string newPasswrod = "";     // 改密交易时的新密码
        public static string rePasswrod = "";      // 改官交易时的重复一遍的新密码
        public static Boolean loginCanceled = false; // 是否取消了登录
        public static int batchNo = 0; // 批次号, 内存变量, 不存储到本地
        public static int traceNo = 0; // 流水号, 内存变量, 不存储到本地
        public static bool login = false;
        public static string current_operator = ""; // 当前操作员的操作员号码，记录交易流水时会用到

        public MainForm()
        {
            InitializeComponent();
            this.KeyPreview = true;
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            switch (e.KeyCode)
            {                 
                case Keys.NumPad1 : //消费    
                    do_payment();
                    break;
                case Keys.NumPad2 : //撤销
                    do_cancel_payment();
                    break;
                case Keys.NumPad3 : //充值
                    do_deposit();
                    break;
                case Keys.NumPad4 : //激活
                    do_new_card();
                    break;
                case Keys.NumPad5 : //积分
                    PointsForm pForm = new PointsForm();
                    pForm.ShowDialog();
                    break;
                case Keys.NumPad6 : //卡改密
                    do_change_password();
                    break;
                case Keys.NumPad7 : //改有效期
                    do_change_overdue_date();
                    break;
                case Keys.NumPad8 : //余额查询
                    //OperatorForm oForm = new OperatorForm();
                    //oForm.ShowDialog();
                    do_check_balance();
                    break;
                case Keys.NumPad9 : //其它
                    OthersForm opForm = new OthersForm();
                    opForm.ShowDialog();
                    break;
            }
        }


        /*
         * 消费交易
         */
        private void do_payment()
        {
            //this.do_reversal(1);
            trans.init();
            trans.Action = "payment";

            InputForm iForm = new InputForm();//刷卡
            iForm.InputType = "card";           
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "amount"; //输入交易金额
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "password"; //输入交易密码
            iForm.ShowDialog();

            trans.Batch_No = Utils.getBatchNum();
            trans.Trace_No = Utils.getTraceNum();

            if (trans.Is_Canceled) return;

            send_trans(trans); //打包并上送交易
        }


        /*
         * 撤销交易         
         */
        private void do_cancel_payment()
        {
            MainForm.trans.init();
            MainForm.trans.Action = "cancel_trans";

            InputForm iForm = new InputForm();

            iForm.InputType = "batch_no"; // 输入批次号
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "trace_no"; // 输入流水号
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "card";
            iForm.ShowDialog(); // 输入卡号
            if (trans.Is_Canceled) return;

            iForm.InputType = "password"; // 持卡人输入密码
            iForm.ShowDialog();

            trans.Batch_No = Utils.getBatchNum();
            trans.Trace_No = Utils.getTraceNum();

            if (trans.Is_Canceled) return;

            send_trans(trans); //打包并上送交易          
        }
        /*
         * 充值交易
         */
        private void do_deposit()
        {
            trans.init();
            trans.Action = "deposit";

            InputForm iForm = new InputForm(); //刷卡
            iForm.InputType = "card";
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "amount"; //输入充值金额
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            //iForm.InputType = "masterPassword"; //输入主管密码
            //iForm.ShowDialog();
            //if (trans.Is_Canceled) return;

            iForm.InputType = "password"; //输入持卡人密码
            iForm.ShowDialog();

            trans.Batch_No = Utils.getBatchNum();
            trans.Trace_No = Utils.getTraceNum();

            if (trans.Is_Canceled) return;

            send_trans(trans); //打包并上送交易
        }


        /*
         * 卡启用(激活)交易
         */
        private void do_new_card()
        {
            trans.init();
            trans.Action = "new_card";

            InputForm iForm = new InputForm(); //刷卡
            iForm.InputType = "card";
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "password"; //输入卡密码
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            trans.Batch_No = Utils.getBatchNum();
            trans.Trace_No = Utils.getTraceNum();

            send_trans(trans); //打包并上送交易
        }


        /*
         * 卡改密交易
         */
        private void do_change_password()
        {
            trans.init();
            trans.Action = "change_password";
            
            InputForm iForm = new InputForm(); //刷卡
            iForm.InputType = "card";
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            //iForm.InputType = "masterPassword"; //输入主管密码
            //iForm.ShowDialog();
            //if (trans.Is_Canceled) return;

            iForm.InputType = "password"; //输入旧密码
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "newpassword"; //输入新密码
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "repassword"; //再输入一遍新密码
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            if (newPasswrod != rePasswrod)
            {
                MessageBox.Show("两次输入密码不一致");
                return;
            }
            trans.NewPassword = newPasswrod;
            trans.ReNewPassword = rePasswrod;

            trans.Batch_No = Utils.getBatchNum();
            trans.Trace_No = Utils.getTraceNum();

            send_trans(trans); //打包并上送交易
        }

        /*
         * 卡改有效期交易
         */
        private void do_change_overdue_date()
        {
            trans.init();
            trans.Action = "change_overdue_date";

            InputForm iForm = new InputForm(); //刷卡
            iForm.InputType = "card";
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "date"; //输入新的有效期
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            iForm.InputType = "password"; //输入持卡人密码
            iForm.ShowDialog();
            if (trans.Is_Canceled) return;

            trans.Batch_No = Utils.getBatchNum();
            trans.Trace_No = Utils.getTraceNum();

            send_trans(trans); //打包并上送交易
        }

        /*
         * 余额查询交易
         */
        private void do_check_balance()
        {
            trans.init();
            trans.Action = "check_balance";
            InputForm iForm = new InputForm();
            iForm.InputType = "card";
            iForm.ShowDialog();
            if (trans.Is_Canceled == true) return;

            iForm.InputType = "password";
            iForm.ShowDialog();
            if (trans.Is_Canceled == true) return;

            trans.Batch_No = Utils.getBatchNum();
            trans.Trace_No = Utils.getTraceNum();

            //String dataPackage = MainForm.trans.Build_Trans_String();
            MainForm.send_trans(MainForm.trans);
        }


        /*
         *  冲正交易
         */
        private void do_reversal(int reversal_times)
        {
            DB db = new DB();
            DataTable dt = new DataTable();
            dt = db.ExecuteReturnSQL("SELECT id, card_no, batch_no, trace_no FROM trans WHERE state='p' AND trans_name IN ('payment', 'deposit', 'cancel_trans', 'points_payment', 'points_deposit')");
            if (dt.Rows.Count > 0)
            {
                this.statusTransText.Text = "冲正";
                this.Refresh();

                String id = dt.Rows[0]["id"].ToString();
                String card_no = dt.Rows[0]["card_no"].ToString();
                String old_batch_no = dt.Rows[0]["batch_no"].ToString();
                String old_trace_no = dt.Rows[0]["trace_no"].ToString();

                trans.init();
                trans.Action = "reversal";
                trans.Old_Batch_No = old_batch_no;
                trans.Old_Trace_No = old_trace_no;
                trans.Card_No = card_no;

                trans.Batch_No = Utils.getBatchNum();
                trans.Trace_No = Utils.getTraceNum();

                string dataPackage = trans.Build_Trans_String();
                MySocket mSocket = new MySocket();
                string rtnString = mSocket.Send(dataPackage);
                // 处理返回结果
                Hashtable hashTable = new Hashtable();
                hashTable = trans.GetReturnPackage(rtnString);
                // 如果返回成功，则更新本地数据表中的交易记录状态为"s"
                string result_code = "";
                foreach (DictionaryEntry de in hashTable)
                {
                    if (de.Key.ToString().Trim() == "result_code")
                    {
                        result_code = de.Value.ToString().Trim();
                    }                   
                }

                if (result_code == "1")
                {
                    db.ExecuteNoReturnSQL(String.Format("UPDATE trans SET state='s' WHERE id='{0}'", id));
                }

                this.statusTransText.Text = "";
                this.Refresh();
            }
            else
            {
                return;
            }
        }

        public static void send_trans(CoolCard.MessagePackage.CardTrans trans)
        {
            // 上送交易前要先添加本地交易流水
            DB db = new DB();
            String guid = Guid.NewGuid().ToString();
            db.AddTrans(guid, trans.Card_No, trans.Action, trans.Batch_No, trans.Trace_No, trans.Amount, current_operator);
            db.ExecuteNoReturnSQL("UPDATE settings SET val = val + 1 WHERE setting = 'current_trace_no'");

            // 上送交易
            string dataPackage = trans.Build_Trans_String();
            MySocket mSocket = new MySocket();
            string rtnString = mSocket.Send(dataPackage);
            // 处理返回结果
            Hashtable hashTable = new Hashtable();
            hashTable = trans.GetReturnPackage(rtnString);
            // 如果返回成功，则更新本地数据表中的交易记录状态为"s"
            string action = "";
            string shop_no = "";
            string terminal_no = "";
            string trans_date = "";
            string trans_time = "";
            string batch_no = "";
            string trace_no = "";
            string result_code = "";            
            foreach (DictionaryEntry de in hashTable)
            {
                if (de.Key.ToString().Trim() == "action")
                {
                    action = de.Value.ToString().Trim();
                }
                if (de.Key.ToString().Trim() == "shop_no")
                {
                    shop_no = de.Value.ToString().Trim();
                }
                if (de.Key.ToString().Trim() == "terminal_no")
                {
                    terminal_no = de.Value.ToString().Trim();
                }
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
                if(de.Key.ToString().Trim() == "batch_no")
                {
                	batch_no = de.Value.ToString().Trim();
                }
                if(de.Key.ToString().Trim() == "trace_no")
                {
                	trace_no = de.Value.ToString().Trim();
                }
            }
            if (action != "settlement")
            {
                if (result_code == "0")
                {
                    db.UpdateTrans(guid, trans_date, trans_time, batch_no, trace_no, "s");
                    PrintTicket(hashTable);
                }
                else
                {
                    MessageBox.Show(result_code.ToString() + ":" + CoolCard.Config.GetConfig("ERRORCODE", result_code), "", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    db.UpdateTrans(guid, trans_date, trans_time, batch_no, trace_no, "f");
                }
            }
            else
            {
                if (result_code == "0" || result_code == "29")
                {
                    if (result_code == "29")
                    {
                        MessageBox.Show("账不平");
                    }

                    int payment_count = db.GetCount("SELECT COUNT(*) FROM trans WHERE trans_name = 'payment' AND state = 's'");
                    int deposit_count = db.GetCount("SELECT COUNT(*) FROM trans WHERE trans_name = 'deposit' AND state = 's'");
                    int points_payment_count = db.GetCount("SELECT COUNT(*) FROM trans WHERE trans_name = 'points_payment' AND state = 's'");
                    int points_deposit_count = db.GetCount("SELECT COUNT(*) FROM trans WHERE trans_name = 'points_deposit' AND state = 's'");

                    int payment_amount = 0;
                    int deposit_amount = 0;
                    int points_payment_amount = 0;
                    int points_deposit_amount = 0;

                    if (payment_count > 0)
                    {
                        payment_amount = db.GetCount("SELECT SUM(amount) FROM trans WHERE trans_name = 'payment' AND state = 's'");
                    }
                    if (deposit_count > 0)
                    {
                        deposit_amount = db.GetCount("SELECT SUM(amount) FROM trans WHERE trans_name = 'deposit' AND state = 's'");
                    }
                    if (points_payment_count > 0)
                    {
                        points_payment_amount = db.GetCount("SELECT SUM(amount) FROM trans WHERE trans_name = 'points_payment' AND state = 's'");
                    }
                    if (points_deposit_count > 0)
                    {
                        points_deposit_amount = db.GetCount("SELECT SUM(amount) FROM trans WHERE trans_name = 'points_deposit' AND state = 's'");
                    }

                    StreamReader sr = new StreamReader(Environment.CurrentDirectory + "/settlement.tpl");
                    string printString = "";
                    printString = sr.ReadToEnd();
                    sr.Close();
                    String settlement_data = "";
                    settlement_data += "消费\t" + payment_count.ToString() + "\t" + payment_amount.ToString() + "\t\n";
                    settlement_data += "充值\t" + deposit_count.ToString() + "\t" + deposit_amount.ToString() + "\t\n";

                    printString = printString.Replace("{shop_num}", shop_no);
                    printString = printString.Replace("{terminal_num}", terminal_no);
                    printString = printString.Replace("{date}", trans_date);
                    printString = printString.Replace("{time}", trans_time);
                    printString = printString.Replace("{settlement_data}", settlement_data);

                    db.ExecuteNoReturnSQL("DELETE FROM trans");
                    db.ExecuteNoReturnSQL("UPDATE settings SET val = val + 1 WHERE setting = 'current_batch_no'");
                    db.ExecuteNoReturnSQL("UPDATE settings SET val = '1' WHERE setting = 'current_trace_no'");

                    MessageBox.Show(printString);
                    //TicketsPrinter ticketsPrinter = new TicketsPrinter();
                    //ticketsPrinter.PrintString = printString;
                    //ticketsPrinter.printTicket();
                }
                else
                {
                    MessageBox.Show(result_code.ToString() + ":" + CoolCard.Config.GetConfig("ERRORCODE", result_code), "", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        //程序启动时要先签到
        private void MainForm_Load(object sender, EventArgs e)
        {
                while (login == false)
                {
                    SignInForm sInForm = new SignInForm();
                    sInForm.ShowDialog();                    
                }
                if (loginCanceled == true)
                {
                    this.Close();
                }
        }

        //打印小票
        private static void PrintTicket(Hashtable hashTable)
        {
            //打印小票前要查看交易是否成功
            //如果交易成功，要更新本地数据库交易表中的交易流水，再打印小票
            StreamReader sr = new StreamReader(Environment.CurrentDirectory + "/template.tpl");
            string printString = "";
            printString = sr.ReadToEnd();
            sr.Close();
            string shop_no = "";
            string terminal_no = "";
            string card_no = "";
            string trans_date = "";
            string trans_time = "";
            string batch_no = "";
            string trace_no = "";
            string trans_name = "";
            double amount = 0.00; ;
            string current_points = "";
            string total_points = "";
            double balance = 0.00;

            string key = "";
            foreach (DictionaryEntry de in hashTable)
            {
                key = de.Key.ToString().Trim();
                if (key == "shop_no")
                {
                    shop_no = de.Value.ToString().Trim();  //返回的商户号
                }
                if (key == "terminal_no")
                {
                    terminal_no = de.Value.ToString().Trim(); // 返回的终端号
                }
                if (key == "card_no")
                {
                	card_no = de.Value.ToString().Trim(); // 返回的卡号
                }
                if (key == "trans_date")
                {
                    trans_date = de.Value.ToString().Trim(); // 返回原交易日期
                }
                if (key == "trans_time")
                {
                    trans_time = de.Value.ToString().Trim(); // 返回的交易时间
                }
                if (key == "batch_no")
                {
                    batch_no = de.Value.ToString().Trim(); // 返回的批次号
                }
                if (key == "trace_no")
                {
                    trace_no = de.Value.ToString().Trim(); // 返回的流水号
                }
                if (key == "trans_code")
                {
                    trans_name = de.Value.ToString().Trim(); // 返回的交易名称(英文)                    
                }
                if (key == "amount")
                {
                    if (de.Value.ToString().Trim() == "")
                    {
                        amount = Convert.ToDouble(0.00);
                    }
                    else
                    {
                        if (trans_name == "000050" || trans_name == "000070" || trans_name == "000060" || trans_name == "000080") //积分相关的交易不能除以100
                        {
                            amount = Convert.ToDouble(de.Value.ToString().Trim());
                        }
                        else
                        {
                            amount = Convert.ToDouble(de.Value.ToString().Trim()) / 100; // 因为金额在系统中是以[分]表示,显示时要转换成[元]
                        }
                    }
                }
                if (key == "current_points")
                {
                    current_points = de.Value.ToString().Trim(); // 本次积分
                }
                if (key == "total_points")
                {
                    total_points = de.Value.ToString().Trim(); // 可用积分
                }
                if (key == "balance")
                {
                    balance = Convert.ToDouble ( de.Value.ToString().Trim())/100; // 可用余额
                }
            }
            
            // printString = string.Format(printString, "商户存根", shop_no, terminal_no, trans_date, trans_time, batch_no,trace_no, CoolCard.Config .GetConfig ("TRANSCODE", trans_name), amount, current_points, total_points, balance, "", "");
            printString = printString.Replace("{shop_num}", shop_no);
            printString = printString.Replace("{terminal_num}", terminal_no);
            printString = printString.Replace("{date}", trans_date);
            printString = printString.Replace("{time}", trans_time);
            printString = printString.Replace("{batch_num}", batch_no);
            printString = printString.Replace("{trace_num}", trace_no);
            printString = printString.Replace("{type}", CoolCard.Config .GetConfig ("TRANSCODE", trans_name));
            printString = printString.Replace("{card_num}", card_no);
            printString = printString.Replace("{amount}", amount.ToString());
            printString = printString.Replace("{current_points}", current_points);
            printString = printString.Replace("{valid_points}", total_points);
            printString = printString.Replace("{balance}", balance.ToString());
            printString = printString.Replace("{remark}", "");
            
            // 不打印
            if (CoolCard.Config .GetConfig("SETTINGS", "ticket_pages", "1") == "0")
            {
            	printString  = printString.Replace("{ticket_type}", "商户存根").Replace("{signature}", "持卡人签名");
                MessageBox.Show(printString);
            }

            // 开始打印
            if (CoolCard.Config .GetConfig("SETTINGS", "ticket_pages", "1") == "1")
            {
                TicketsPrinter ticketsPrinter = new TicketsPrinter();
                ticketsPrinter.PrintString = printString.Replace("{ticket_type}", "商户存根").Replace("{signature}", "持卡人签名");
                ticketsPrinter.printTicket();
            }

            // 打印第二联
            if (CoolCard.Config .GetConfig("SETTINGS", "ticket_pages", "1") == "2")
            {
                Thread.Sleep(3000);
                TicketsPrinter ticketsPrinter = new TicketsPrinter();
                ticketsPrinter.PrintString = printString.Replace("{ticket_type}", "持卡人留存").Replace("{signature}", "");
                ticketsPrinter.printTicket();
            }
        }
    }
}