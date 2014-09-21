using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace CoolCard
{
    public partial class OthersForm : Form
    {
        public OthersForm()
        {
            InitializeComponent();
        }

        private void OthersForm_KeyDown(object sender, KeyEventArgs e)
        {
            //检查是否取消了交易
            Config cfg = new Config();
            if (e.KeyValue.ToString() == cfg.getCancelKeyValue())
            {                
                this.Close();
            }

            switch (e.KeyCode)
            { 
                case Keys .NumPad1:
                    do_settlement();
                    break;
                case Keys .NumPad2:
                    do_bind_member();
                    break;
            }
        }

        private void do_bind_member()
        {
            MemberBindForm mbf = new MemberBindForm();
            mbf.Show();
        }

        private void do_settlement()
        {
            if (MessageBox.Show("确定结算?", "", MessageBoxButtons.OKCancel) == DialogResult.OK)
            {
                DB db = new DB();

                int trace_count = db.GetCount("SELECT COUNT(*) FROM trans WHERE state = 's' AND (trans_name = 'payment' OR trans_name =  'deposit' OR trans_name = 'points_payment' OR trans_name = 'points_deposit')");
                if (trace_count == 0)
                {
                    MessageBox.Show("无交易流水");
                    return;
                }

                int payment_count = db.GetCount("SELECT COUNT(*) FROM trans WHERE trans_name = 'payment' AND state = 's'");
                int deposit_count = db.GetCount("SELECT COUNT(*) FROM trans WHERE trans_name = 'deposit' AND state = 's'");
                int points_payment_count = db.GetCount("SELECT COUNT(*) FROM trans WHERE trans_name = 'points_payment' AND state = 's'");
                int points_deposit_count = db.GetCount("SELECT COUNT(*) FROM trans WHERE trans_name = 'points_deposit' AND state = 's'");

                int payment_amount = 0;
                int deposit_amount= 0;
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

                MainForm.trans.init();
                MainForm.trans.Action = "settlement";
                MainForm.trans.Batch_No = Utils.getBatchNum();
                MainForm.trans.Trace_No = Utils.getTraceNum();
                MainForm.trans.Payment_Count = payment_count.ToString();
                MainForm.trans.Payment_Amount = payment_amount.ToString();
                MainForm.trans.Deposit_Count = deposit_count.ToString();
                MainForm.trans.Deposit_Amount = deposit_amount.ToString();
                MainForm.trans.Points_Payment_Count = points_payment_count.ToString();
                MainForm.trans.Points_Payment_Amount = points_payment_amount.ToString();
                MainForm.trans.Points_Deposit_Count = points_deposit_count.ToString();
                MainForm.trans.Points_Deposit_Amount = points_deposit_amount.ToString();

                MainForm.send_trans(MainForm.trans);

            }
        }
    }
}