using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace CoolCard
{
    public partial class OperatorPasswordForm : Form
    {
        public OperatorPasswordForm()
        {
            InitializeComponent();
        }

        private void btnOK_Click(object sender, EventArgs e)
        {
            string password = this.txtOldPassword.Text.Trim();          // ԭ����
            string newPassword = this.txtNewPassword.Text.Trim();       // ������
            string reNewPassword = this.txtReNewPassword.Text.Trim();   // �ظ�������

            if (newPassword != reNewPassword)  // �������������������Ƿ�һ��
            {
                MessageBox.Show("��������������벻һ��!");
                return;
            }

            DB db = new DB();
            DataTable dt = new DataTable();
            dt = db.ExecuteReturnSQL("SELECT password FROM operators WHERE operator_no = '" + MainForm.current_operator + "'");
            if (dt.Rows.Count > 0)
            {
                if (password == dt.Rows[0][0].ToString().Trim())
                {
                    db.ExecuteNoReturnSQL("UPDATE operators SET password = '" + newPassword + "' WHERE operator_no = '" + MainForm.current_operator + "'");
                }
                else
                {
                    MessageBox.Show("ԭ���벻��ȷ!");
                }
            }
            else
            {
                MessageBox.Show("����Ա������!");
            }
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}