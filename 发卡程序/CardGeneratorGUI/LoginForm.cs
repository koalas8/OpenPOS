using System;
using System.Windows.Forms;

namespace CardGeneratorGUI
{
    public partial class LoginForm : Form
    {
        public LoginForm()
        {
            InitializeComponent();
        }

        private void btnLogin_Click(object sender, EventArgs e)
        {
            var userNum = txtUserNum.Text.Trim();
            var password = txtPassword.Text.Trim();

            if (userNum == "")
            {
                MessageBox.Show("用户名不能为空");
                return;
            }
            if (password == "")
            {
                MessageBox.Show("密码不能为空");
                return;
            }

            // TODO: 判断当前登录用户是否有发卡权限

            if (CardGenerator.User.login(userNum, password))
            {
                Close();
                MainForm.LoginFlag = true;
            }

        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            Close();
            MainForm.CancelLoginFlag = true;           
        }
    }
}
