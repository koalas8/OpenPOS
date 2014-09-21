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
            if (e.KeyValue.ToString() == cfg.getCancelKeyValue()) //����Ƿ�ȡ���˽���
            {
                this.Close();
            }
            else if (e.KeyCode == Keys.NumPad1) // ����
            {
                do_settlement();
            }
            else if (e.KeyCode == Keys.NumPad2) // ����Ա������
            {
                do_change_password();
            }
            else if (e.KeyCode == Keys.NumPad3) // ��Ӳ���Ա 
            {
                do_add_operator();
            }
        }

        /*
         * ����
         */
        private void do_settlement()
        {
            if (MessageBox.Show("ȷ������?", "", MessageBoxButtons.OKCancel) == DialogResult.OK)
            {
                MainForm.trans.init();
                MainForm .trans.Action = "settlement";
                string dataPackage = MainForm.trans.Build_Trans_String();
                // ���ͽ���
                MySocket mSocket = new MySocket();
                string rtnString = mSocket.Send(dataPackage);
                // ��ӡͳ�Ƶ�

            }
        }

        /*
         *  ����Ա������ 
         */
        private void do_change_password()
        {
            OperatorPasswordForm opForm = new OperatorPasswordForm();
            opForm.ShowDialog();
        }

        /*
         *  ��Ӳ���Ա
         */

        private void do_add_operator()
        {
            AddOperatorForm aoForm = new AddOperatorForm();
            aoForm.ShowDialog();
        }
    }
}