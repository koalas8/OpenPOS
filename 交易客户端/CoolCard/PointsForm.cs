using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace CoolCard
{
    public partial class PointsForm : Form
    {
        public PointsForm()
        {
            InitializeComponent();
            this.KeyPreview = true;
            this.ControlBox = false;
        }

        private void PointsForm_KeyDown(object sender, KeyEventArgs e)
        {
            //检查是否取消了交易
            Config cfg = new Config();
            if (e.KeyValue.ToString() == cfg.getCancelKeyValue())
            {
                this.Close();
            }
            else if (e.KeyCode == Keys.NumPad1) //积分消费
            {
                do_points_payment();
            }
            else if (e.KeyCode == Keys.NumPad2) //积分充值(积分累计)
            {
                do_points_deposit();
            }
        }

        /*
         *积分消费交易 
         */
        private void do_points_payment()
        {
            MainForm.trans.init();
            MainForm.trans.Action = "points_payment";
            InputForm iForm = new InputForm();
            iForm.InputType = "card"; //刷卡
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            iForm.InputType = "point"; //输入消费积分
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            iForm.InputType = "password"; // 持卡人输入密码
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            //String dataPackage = MainForm.trans.Build_Trans_String();

            MainForm.trans.Batch_No = Utils.getBatchNum();
            MainForm.trans.Trace_No = Utils.getTraceNum();

            MainForm.send_trans(MainForm.trans);
        }


        /*
         * 积分充值(积分累计)交易
         */
        private void do_points_deposit()
        {
            MainForm.trans.init();
            MainForm.trans.Action = "points_deposit";
            InputForm iForm = new InputForm();
            iForm.InputType = "card"; //刷卡
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            iForm.InputType = "point"; //输入充值积分
            iForm.ShowDialog();
            if (MainForm.trans.Is_Canceled) return;

            //iForm.InputType = "master"; //输入主管密码
            //iForm.ShowDialog();
            //if (MainForm.trans.Is_Canceled) return;

            iForm.InputType = "password"; //持卡人输入密码
            iForm.ShowDialog();
            if(MainForm.trans.Is_Canceled) return;

            //String dataPackage = MainForm.trans.Build_Trans_String();

            MainForm.trans.Batch_No = Utils.getBatchNum();
            MainForm.trans.Trace_No = Utils.getTraceNum();

            MainForm .send_trans (MainForm.trans);
        }
                
    }
}