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
            string password = this.txtOldPassword.Text.Trim();          // 原密码
            string newPassword = this.txtNewPassword.Text.Trim();       // 新密码
            string reNewPassword = this.txtReNewPassword.Text.Trim();   // 重复新密码

            if (newPassword != reNewPassword)  // 检查两次输入的新密码是否一致
            {
                MessageBox.Show("两次输入的新密码不一致!");
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
                    MessageBox.Show("原密码不正确!");
                }
            }
            else
            {
                MessageBox.Show("操作员不存在!");
            }
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}