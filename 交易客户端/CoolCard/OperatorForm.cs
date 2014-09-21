using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace CoolCard
{
    public partial class OperatorForm : Form
    {
        public OperatorForm()
        {
            InitializeComponent();
        }

        private void OperatorForm_KeyDown(object sender, KeyEventArgs e)
        {            
            Config cfg = new Config();
            if (e.KeyValue.ToString() == cfg.getCancelKeyValue()) //检查是否取消了交易
            {
                this.Close();
            }
            else if (e.KeyCode == Keys.NumPad1) // 结算
            {
                do_settlement();
            }
            else if (e.KeyCode == Keys.NumPad2) // 操作员改密码
            {
                do_change_password();
            }
            else if (e.KeyCode == Keys.NumPad3) // 添加操作员 
            {
                do_add_operator();
            }
        }

        /*
         * 结算
         */
        private void do_settlement()
        {
            if (MessageBox.Show("确定结算?", "", MessageBoxButtons.OKCancel) == DialogResult.OK)
            {
                MainForm.trans.init();
                MainForm .trans.Action = "settlement";
                string dataPackage = MainForm.trans.Build_Trans_String();
                // 上送交易
                MySocket mSocket = new MySocket();
                string rtnString = mSocket.Send(dataPackage);
                // 打印统计单

            }
        }

        /*
         *  操作员改密码 
         */
        private void do_change_password()
        {
            OperatorPasswordForm opForm = new OperatorPasswordForm();
            opForm.ShowDialog();
        }

        /*
         *  添加操作员
         */

        private void do_add_operator()
        {
            AddOperatorForm aoForm = new AddOperatorForm();
            aoForm.ShowDialog();
        }
    }
}