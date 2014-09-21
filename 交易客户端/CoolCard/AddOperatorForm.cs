using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace CoolCard
{
    public partial class AddOperatorForm : Form
    {
        public AddOperatorForm()
        {
            InitializeComponent();
        }

        private void AddOperatorForm_Load(object sender, EventArgs e)
        {

        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btnOK_Click(object sender, EventArgs e)
        {
            string operatorNo = this.txtOperatorNo.Text.Trim();
            string password = this.txtPassword.Text.Trim();
            string rePassword = this.txtRePassword.Text.Trim();

            if (operatorNo == "")
            {
                MessageBox.Show("����Ա�Ų���Ϊ��!");
                return;
            }

            if (password != rePassword)
            {
                MessageBox.Show("������������벻һ��!");
                return;
            }


            DB db = new DB();
            DataTable dt = new DataTable();
            dt = db.ExecuteReturnSQL("SELECT * FROM operators WHERE operator_no = '" + operatorNo + "'");
            if (dt.Rows.Count > 0)
            {
                MessageBox.Show("�˲���Ա�Ѵ���!");
            }
            else
            {
                if (db.ExecuteNoReturnSQL("INSERT INTO operators (operator_no, password) VALUES ('" + operatorNo + "', '" + password + "')"))
                {
                    MessageBox.Show("��Ӳ���Ա�ɹ�!");
                }
                else
                {
                    MessageBox.Show("��Ӳ���Աʧ��!");
                }
            }

        }
    }
}